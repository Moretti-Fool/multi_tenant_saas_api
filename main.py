from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from config import settings
from database import engine
from models import Base
from models import Tenant, UserVerification, AuditLog
from routes import registration, login, admin, google



app = FastAPI()

# Base.metadata.create_all(
#     bind=engine, 
#     tables=[Tenant.__table__, UserVerification.__table__, AuditLog.__table__]  # Only create Tenant in public
# )


origins = ["*"]

# app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY_GOOGLE_AUTH, same_site="lax")
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,  # Must be a secure, unchanging value
    session_cookie="session_cookie",  # Optional: Customize cookie name
    same_site="lax",                 # Adjust for your environment
    https_only=False                 # Set to True in production
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(registration.router)
app.include_router(login.router)
app.include_router(admin.router)
app.include_router(google.router)




@app.get("/")
def root():
    return {"Message": "Welcome!"}