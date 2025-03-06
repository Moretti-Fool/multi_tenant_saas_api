from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_tenant_db, get_default_db
from models import Tenant, User
from utils.auth import create_access_token, verify_password


router = APIRouter(
    tags=["Login"]
)

@router.post("/login")
def login(
    response: Response, 
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_default_db)
):
    if not user_credentials.username or not user_credentials.password:
        raise HTTPException(status_code=422, detail="Missing required fields")

    tenants = db.query(Tenant).all()
    valid_entry = None
    tenant_name = None  # Store tenant name for cookies

    for entry in tenants:
        tenant_db = next(get_tenant_db(entry.schema_name))  # Ensure this function works correctly

        user = tenant_db.query(User).filter(User.email == user_credentials.username).first()

        if user and verify_password(user_credentials.password, user.hashed_password):
            valid_entry = user
            tenant_name = entry.name  # Assuming the tenant model has a `name` field
            break  # Stop searching once a valid tenant is found

    if not valid_entry:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Ensure the user has a verified account if required
    if not valid_entry.is_verified:
        raise HTTPException(status_code=400, detail="Not registered or verified")

    # Generate Access Token
    access_token = create_access_token(data={"user_id": valid_entry.id})

    # Set Cookies securely
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Strict")
    response.set_cookie(key="tenant_name", value=tenant_name, httponly=False, secure=True, samesite="Strict")

    return {"message": "Login successful", "access_token": access_token}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("tenant_name")
    return {"message": "Logged out successfully"}