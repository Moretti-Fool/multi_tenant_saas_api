
from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_default_db
from models import AuditLog, Role, User
from utils.auth import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(get_current_admin_user),
    tenant_name: str = Cookie(None),
    db: Session =  Depends(get_default_db)
):
    db.add(AuditLog(
        event="ADMIN DASHBOARD",
        tenant_id=current_user.tenant_id,
        details=f"ADMIN {current_user.email} ACCESSING DASHBOARD "
        ))
    db.commit()  
    return {"message": f"Welcome Admin {current_user.email}!"}
