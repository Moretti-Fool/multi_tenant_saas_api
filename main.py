from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from config import settings
from routes import registration, login, admin, google



app = FastAPI(

    redoc_url="/redoc",
    docs_url="/doc",
    openapi_url="/openapi.json"
)

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




templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Route to serve the index page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to Swagger UI
@app.get("/doc")
async def custom_docs():
    return RedirectResponse(url="/swagger")

# Route to ReDoc
@app.get("/redoc")
async def custom_redoc():
    return RedirectResponse(url="/redoc")
