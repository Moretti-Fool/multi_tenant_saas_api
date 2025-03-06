from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    execution_options={"schema_translate_map": {"tenant": "default_schema"}}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()




def get_tenant_db(tenant_schema: str = "public"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        execution_options={"schema_translate_map": {"tenant": tenant_schema}}
    )
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_default_db():
    return next(get_tenant_db("public"))