from datetime import datetime
from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, Integer, String, ForeignKey, text
from sqlalchemy.orm import relationship
from database import Base  # Single base for all models

# Tenant Model in Public Schema
class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = {'schema': 'public'}  # Explicit schema

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    schema_name = Column(String, unique=True, nullable=False)
    
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")


class UserVerification(Base):
    __tablename__ = "user_verifications"
    __table_args__ = {'schema': 'public'}

    token = Column(String, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('public.tenants.id', ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    event = Column(String)  # e.g., "VERIFICATION_SUCCESS"
    tenant_id = Column(Integer, ForeignKey('public.tenants.id', ondelete="CASCADE"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String)

class Admin(Base):
    __tablename__ = "admins"
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_superadmin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    last_login = Column(DateTime, nullable=True)

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {'schema': 'tenant'}  # Default tenant schema

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="role", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'tenant'}  # Default tenant schema

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('tenant.roles.id', ondelete="SET NULL"))  # Allow NULL on role deletion
    tenant_id = Column(Integer, ForeignKey('public.tenants.id', ondelete="CASCADE"))  # Public schema reference
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    verification_token = Column(String, unique=True, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)

    role = relationship("Role", back_populates="users")
    tenant = relationship("Tenant", back_populates="users")

