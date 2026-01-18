"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, tasks, reminders, cron
from app.dependencies import get_db
import os

app = FastAPI(
    title="Task Management API",
    description="API for task management application",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to actual domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["reminders"])
app.include_router(cron.router, prefix="/api/cron", tags=["cron"])


@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "task-management-api",
        "timestamp": "2026-01-18T00:00:00Z",
    }


@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup."""
    # Database connection is handled via dependencies
    print("API server starting...")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown."""
    print("API server shutting down...")
