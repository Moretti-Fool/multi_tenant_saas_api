import re
import uuid
from fastapi import Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from database import engine, SQLALCHEMY_DATABASE_URL, get_tenant_db
from models import Role, Tenant, Base





def create_tenant_schema(schema_name: str):
    # Create the schema
    with engine.connect() as conn:
        conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"'))
        conn.commit()
    
    # Create tenant-specific tables with schema translation
    tenant_engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        execution_options={"schema_translate_map": {"tenant": schema_name}}
    )
    
    # Create tables using the tenant-aware engine
    with tenant_engine.begin() as conn:

        Base.metadata.create_all(conn)

def create_tenant(name: str, db: Session = Depends(get_tenant_db)):
    """Creates a new tenant with a unique schema name and a default USER role."""
    schema_name = re.sub(r"[^a-zA-Z0-9_]", "", name.lower().replace(" ", "_")) + "_" + str(uuid.uuid4())[:8]

    # Check if tenant already exists
    existing_tenant = db.query(Tenant).filter(Tenant.name == name).first()
    if existing_tenant:
        raise HTTPException(status_code=400, detail="Tenant already exists")

    # Create schema
    try:
        create_tenant_schema(schema_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating schema: {str(e)}")

    # Insert the tenant record in the public schema
    new_tenant = Tenant(name=name, schema_name=schema_name)
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)

    # create a fresh session tied to the tenant schema
    tenant_db = next(get_tenant_db(new_tenant.schema_name))

    try:
        # Check if "USER" role exists, if not create it
        if not tenant_db.query(Role).filter(Role.name == "USER").first():
            user_role = Role(name="USER")
            tenant_db.add(user_role)
            tenant_db.commit()
    except Exception as e:
        tenant_db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating default role: {str(e)}")
    finally:
        tenant_db.close()

    return new_tenant

