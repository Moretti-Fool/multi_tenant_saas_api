from datetime import datetime
from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database import get_default_db
from models import AuditLog, User, Admin
from utils.admin_utils import create_admin_token, get_current_admin
from utils.auth import verify_password

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/login")
def admin_login(
    response: Response,
    email: str,
    password: str,
    db: Session = Depends(get_default_db)
):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin or not verify_password(password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Update last login
    admin.last_login = datetime.utcnow()
    db.commit()
    
    # return {
    #     "access_token": create_admin_token(admin.id),
    #     "token_type": "bearer"
    # }
    access_token = create_admin_token(admin.id) 
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Strict")



@router.get("/dashboard")
def admin_dashboard(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_default_db)
):
    db.add(AuditLog(
        event="ADMIN_DASHBOARD_ACCESS",
        details=f"Admin {current_admin.email} accessed dashboard"
    ))
    db.commit()
    return {"message": f"Welcome Admin {current_admin.email}!"}



@router.get("/auditlog")
def get_audit_log(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_default_db)
):
    audit_logs = db.query(AuditLog).all()
    return audit_logs