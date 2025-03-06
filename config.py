from pydantic_settings import BaseSettings


class Settings(BaseSettings): # CASE INSENSITIVE BUT BEST PRACTICE IS TO SET THEM CAPITALIZE
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    BASE_URL: str
    SECRET_KEY: str 
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    POOL_SIZE: int
    MAX_OVERFLOW: int
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    SECRET_KEY_GOOGLE_AUTH: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_EMAIL: str
    SMTP_PASSWORD: str
    VERIFICATION_TOKEN_EXPIRE: int
    
    
    
    
    class Config:
        env_file = ".env"

settings =  Settings()