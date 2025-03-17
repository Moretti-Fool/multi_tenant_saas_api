import datetime
import secrets
from datetime import datetime, timedelta
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from config import settings
from database import get_default_db, get_tenant_db
from models import Tenant, User,Role, UserVerification, AuditLog
from schemas import UserCreate
from services.tenant_services import create_tenant
from utils.auth import get_password_hash
from utils.email import send_email


router = APIRouter(
    prefix="/register",
    tags=["Registration"]

)




@router.post("/")
async def register_user(
    request: Request,
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_default_db)
):
    # Tenant management
    tenant = db.query(Tenant).filter(Tenant.name == user.tenant_name).first()
    if not tenant:
        tenant = create_tenant(user.tenant_name, db)
        # initialize_tenant_schema(tenant.schema_name, db)

    # if not schema_exists(db, tenant.schema_name):
    #     raise HTTPException(500, "Tenant schema not initialized")

    # Token generation
    raw_token = secrets.token_urlsafe(32)
    hashed_token = bcrypt.hashpw(raw_token.encode(), bcrypt.gensalt()).decode()

    # Tenant database connection
    tenant_db = next(get_tenant_db(tenant.schema_name))
    user_query = tenant_db.query(User).filter(User.email == user.email).first()
    if(user_query):
        raise HTTPException(status_code=400, detail=f"Email {user.email} already exists")
    try:
        # User creation
        default_role = tenant_db.query(Role).filter(Role.name == "USER").first()
        if not default_role:
            raise HTTPException(500, "Default role not found")

        new_user = User(
            email=user.email,
            hashed_password=get_password_hash(user.password),
            role_id=default_role.id,
            tenant_id=tenant.id,
            verification_token=hashed_token,
            token_expires_at=datetime.utcnow() + timedelta(minutes=settings.VERIFICATION_TOKEN_EXPIRE)
        )

        tenant_db.add(new_user)
        tenant_db.commit()

        # Store verification token in public schema
        verification_entry = UserVerification(
            token=hashed_token,
            tenant_id=tenant.id,
            expires_at=new_user.token_expires_at
        )
        db.add(verification_entry)
        db.commit()

        # Audit log
        db.add(AuditLog(
            event="USER_REGISTERED",
            tenant_id=tenant.id,
            details=f"User {user.email} registered"
        ))
        db.commit()

    except Exception as e:
        tenant_db.rollback()
        db.rollback()
        raise HTTPException(500, f"Registration failed: {str(e)}")
    finally:
        tenant_db.close()

    # Send verification email
    verification_link = f"{sttings.BASE_URL}/register/verify-email?token={raw_token}"
    email_body = f"""
    <html>
        <body>
            <h3>Welcome to Our App!</h3>
            <p>Click the link below to verify your email:</p>
            <a href="{verification_link}">Verify Email</a>
        </body>
    </html>
    """
    # background_tasks.add_task(send_email, user.email, "Verify Your Email", email_body)
    background_tasks.add_task(send_email, user.email, "Verify Your Email", email_body)

    return {"message": "Registration successful. Check your email for verification."}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_default_db)):
    # Get all active verification entries
    verification_entries = db.query(UserVerification).filter(
        UserVerification.expires_at > datetime.utcnow(),
        UserVerification.is_used == False
    ).all()

    # Check if any entry matches the token
    valid_entry = None
    for entry in verification_entries:
        if bcrypt.checkpw(token.encode(), entry.token.encode()):
            valid_entry = entry
            break

    if not valid_entry:
        db.add(AuditLog(
            event="VERIFICATION_FAILED",
            tenant_id=None,
            details="Invalid or expired token"
        ))
        db.commit()
        raise HTTPException(400, "Invalid or expired token")

    tenant = db.query(Tenant).get(valid_entry.tenant_id)
    if not tenant:
        db.add(AuditLog(
            event="VERIFICATION_FAILED",
            tenant_id=valid_entry.tenant_id,
            details="Tenant not found"
        ))
        db.commit()
        raise HTTPException(400, "Invalid tenant")

    tenant_db = next(get_tenant_db(tenant.schema_name))
    try:
        user = tenant_db.query(User).filter(
            User.verification_token == valid_entry.token,
            User.token_expires_at > datetime.utcnow()
        ).first()

        if not user or user.is_verified:
            raise HTTPException(400, "Invalid or expired token")

        # Update records
        user.is_verified = True
        user.verification_token = None
        user.token_expires_at = None
        valid_entry.is_used = True

        tenant_db.commit()
        db.commit()

        # Audit logs
        db.add_all([
            AuditLog(
                event="USER_VERIFIED",
                tenant_id=tenant.id,
                details=f"User {user.email} verified"
            ),
            AuditLog(
                event="VERIFICATION_SUCCESS",
                tenant_id=tenant.id,
                details="Email verification completed"
            )
        ])
        db.commit()

        return {"message": "Email successfully verified."}

    except Exception as e:
        tenant_db.rollback()
        db.rollback()
        db.add(AuditLog(
            event="VERIFICATION_ERROR",
            tenant_id=tenant.id,
            details=str(e)
        ))
        db.commit()
        raise HTTPException(500, f"Verification failed: {str(e)}")
    finally:
        tenant_db.close()
