"""
Database configuration and session management.
Using SQLite for local development.
"""

from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration - Use SQLite for local development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./todoapp.db"
)

# Create database engine
# For SQLite, we need to handle connection args differently
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=os.getenv("SQL_ECHO", "False").lower() == "true"
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
        pool_recycle=3600,
        echo=os.getenv("SQL_ECHO", "False").lower() == "true"
    )

# Session factory for database operations
SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


def get_db():
    """
    Dependency to get database session.
    Usage in FastAPI: Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables.
    Call this during application startup.
    """
    from . import models
    SQLModel.metadata.create_all(engine)


def drop_tables():
    """
    Drop all database tables.
    Use with caution - destructive operation!
    """
    from . import models
    SQLModel.metadata.drop_all(engine)
