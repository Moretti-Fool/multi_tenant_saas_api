from pydantic_settings import BaseSettings
from pydantic import EmailStr

class UserCreate(BaseSettings):
    email: EmailStr
    password: str
    tenant_name: str
