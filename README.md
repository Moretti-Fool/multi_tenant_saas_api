# Multi-Tenant SaaS Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.11-green)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-blue)](https://www.postgresql.org)

A secure, scalable multi-tenant application with schema-based isolation, featuring robust authentication and admin management.

## ✨ Key Features

- **Multi-Tenant Architecture**
  - PostgreSQL schema isolation
  - Automated tenant provisioning
  - Per-tenant database connections

- **Authentication & Security**
  - JWT token authentication
  - Google OAuth 2.0 integration
  - BCrypt password hashing
  - Email verification flow

- **Admin Features**
  - Audit logging system
  - Superadmin privileges
  - User activity monitoring

- **DevOps Ready**
  - Docker containerization
  - Alembic database migrations
  - Environment variable configuration

## 🚀 Getting Started

### Installation

1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/multi-tenant-saas.git
cd multi-tenant-saas
```

2️⃣ Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

4️⃣ Setup Environment Variables
```bash
Rename .env.example to .env and update the database credentials.
```

5️⃣ Run Database Migrations
```bash
alembic upgrade head
```

6️⃣ Initialize Admin User  
```bash
python admin_create.py create-admin
```

7️⃣ Start the Application
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

##🐳 Docker Setup

### To run the application using Docker:
```bash
docker-compose -f docker-compose-prod.yml up --build
```
