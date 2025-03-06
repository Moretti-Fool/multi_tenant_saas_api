from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_tenant_db
from models import Role, User
from utils.auth import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(get_current_admin_user),
    tenant_name: str = Cookie(None)
):
    return {"message": f"Welcome Admin {current_user.email}!"}
