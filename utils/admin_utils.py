from fastapi import Cookie, HTTPException, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from config import settings
from database import get_default_db
from models import Admin
from utils.auth import create_access_token


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def get_current_admin(
    access_token: str = Cookie(None),
    db: Session = Depends(get_default_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing access token")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        admin_id: int = payload.get("admin_id")
        if admin_id is None:
            raise HTTPException(status_code=401, detail="Invalid admin credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin or not admin.is_active:
        raise HTTPException(status_code=401, detail="Admin not found or inactive")
    
    return admin

def create_admin_token(admin_id: int):
    return create_access_token(data={"admin_id": admin_id})