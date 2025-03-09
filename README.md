# Multi-Tenant SaaS Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.11-green)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-blue)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-20.10%2B-blue)](https://www.docker.com)

A scalable Multi-Tenant SaaS application built with FastAPI and PostgreSQL schema-based isolation, featuring secure authentication, tenant management, and admin controls.

## Features

- **Multi-Tenant Architecture**: Schema isolation per tenant using PostgreSQL
- **Authentication**:
  - JWT-based authentication
  - Google OAuth2 integration
  - Password hashing with bcrypt
- **Tenant Management**:
  - Automated schema creation
  - Default role initialization (USER)
  - Tenant-specific databases
- **Admin Features**:
  - Superadmin controls
  - Audit logging system
  - Admin dashboard
- **Email Verification**: Secure token-based verification flow
- **Containerization**: Docker + Docker Compose for development/production
- **Alembic Migrations**: For database versioning

## Tech Stack

- **Backend**: Python 3, FastAPI
- **Database**: PostgreSQL, SQLAlchemy ORM
- **Auth**: JWT, OAuth2, Google Auth
- **Infra**: Docker, Docker Compose
- **Other**: Alembic (migrations), Pydantic (validation), SMTP email

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Docker 20.10+

## 🛠️ Installation
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Moretti-Fool/multi_tenant_saas_api.git
cd multi-tenant-saas
```

### **2️⃣ Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Setup Environment Variables**
Rename `.env.example` to `.env` and update the database credentials.

### 5️⃣ Create Admin User**
```bash
python admin_create.py create-admin
```

### **6️⃣ Start the Application**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🐳 Docker Setup
```bash
docker-compose -f docker-compose-prod.yml up --build -d
```

