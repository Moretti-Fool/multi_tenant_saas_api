from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth, OAuthError
from sqlalchemy.orm import Session
from config import settings
from database import get_tenant_db, get_default_db
from models import AuditLog, Role, Tenant, User
from services.tenant_services import create_tenant
from utils.auth import create_access_token, generate_placeholder_password, get_current_tenant_user

router = APIRouter(prefix="/google", tags=["GOOGLE AUTH"])
oauth = OAuth()

# Configure Google OAuth
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    redirect_uri=settings.GOOGLE_REDIRECT_URI,
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account',
    }
)

@router.get("/login")
async def login(request: Request, tenant_name: str, action: str = "login"):
    if action not in ["login", "register"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    # Store context in session
    request.session.update({
        "tenant_name": tenant_name,
        "action": action,
        "next_url": request.query_params.get("next", "/")
    })
    
    return await oauth.google.authorize_redirect(request, settings.GOOGLE_REDIRECT_URI)

@router.get("/callback")
async def callback(request: Request, db: Session = Depends(get_default_db)):

    try:
        # Retrieve OAuth token and validate state
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        email = user_info.get("email")
        
        if not email:
            raise HTTPException(status_code=422, detail="Missing email in Google response")
            
        # Retrieve stored session data
        tenant_name = request.session.get("tenant_name")
        action = request.session.get("action")
        
        if not tenant_name or not action:
            raise HTTPException(status_code=400, detail="Missing session context")

    except OAuthError as e:
        raise HTTPException(status_code=401, detail=f"OAuth error: {str(e)}")

    # Get tenant database connection
    tenant_db = next(get_tenant_db(tenant.schema_name))
    tenant = db.query(Tenant).filter(Tenant.name == tenant_name).first()
    if not tenant:
        tenant = create_tenant(tenant_name, db)
    try:
        default_role = tenant_db.query(Role).filter(Role.name == "USER").first()
        if not default_role:
            raise HTTPException(500, "Default role not found")

    # Handle registration flow
        if action == "register":
            existing_user = tenant_db.query(User).filter(User.email == email).first()
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="User already exists in this tenant"
                )
                
            # Create new user
            new_user = User(
                email=email,
                hashed_password=generate_placeholder_password(),
                role_id=default_role.id,
                tenant_id=tenant.id,
                verification_token=None,
                token_expires_at=None,
                is_verified=True
            )

            tenant_db.add(new_user)
            tenant_db.commit()
            valid_entry = new_user

            # Add audit log
            db.add(AuditLog(
                event="USER_SIGN_UP",
                tenant_id=tenant.id,
                details=f"User {email} registered via Google"
            ))

    # Handle login flow
        elif action == "login":
            valid_entry = tenant_db.query(User).filter(User.email == email).first()
            if not valid_entry:
                raise HTTPException(
                    status_code=404,
                    detail="No user found in this tenant"
                )

        # Common post-auth actions
        db.add(AuditLog(
            event="USER_LOGIN",
            tenant_id=tenant.id,
            details=f"User {email} logged in via Google"
        ))
        db.commit()
    except:
        tenant_db.rollback()
        db.rollback()
    # Generate tokens
    access_token = create_access_token(data={"user_id": valid_entry.id})
    response = JSONResponse(content={"message": "Authentication successful"})
    
    # Set cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Strict"
    )
    response.set_cookie(
        key="tenant_name",
        value=tenant.name,
        httponly=False,
        secure=True,
        samesite="Strict"
    )

    return response

@router.post("/logout")
def logout(
    response: Response,
    current_user: User = Depends(get_current_tenant_user),
    db: Session = Depends(get_default_db)
):
    """Logout endpoint remains mostly the same"""
    response.delete_cookie("access_token")
    response.delete_cookie("tenant_name")

    db.add(AuditLog(
        event="USER_LOGOUT",
        tenant_id=current_user.tenant_id,
        details=f"User {current_user.email} logged out"
    ))
    db.commit()

    return {"message": "Logged out successfully"}
