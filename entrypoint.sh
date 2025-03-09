#!/bin/sh

# Wait for PostgreSQL to be ready
sleep 5

# Run Alembic migrations
alembic upgrade head

# Start the FastAPI server
exec uvicorn main:app --host 0.0.0.0 --port 8000
