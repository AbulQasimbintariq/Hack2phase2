"""
FastAPI application for Vercel serverless.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, tasks, reminders, cron
from app.database import create_tables
import os

# Create tables on import (serverless)
create_tables()

app = FastAPI(
    title="Task Management API",
    description="API for task management application with authentication, tasks, and reminders",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://hakathon2-ii.vercel.app",  # Add your Vercel domain
        "*"  # For development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["reminders"])
app.include_router(cron.router, prefix="/api/cron", tags=["cron"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Task Management API",
        "status": "running",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring."""
    from datetime import datetime
    return {
        "status": "healthy",
        "service": "task-management-api",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }