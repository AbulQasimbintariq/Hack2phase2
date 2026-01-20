"""
Database models for the Todo application.
Using SQLModel for Pydantic + SQLAlchemy integration.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import uuid4

from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DateTime, func, String, Table, ForeignKey


# Enums
class Priority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RecurrenceType(str, Enum):
    """Task recurrence types."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


# Association table for many-to-many relationship between Task and Tag
class TaskTag(SQLModel, table=True):
    """Association table for Task-Tag many-to-many relationship."""
    __tablename__ = "task_tag"

    task_id: str = Field(foreign_key="task.id", primary_key=True)
    tag_id: str = Field(foreign_key="tag.id", primary_key=True)


class User(SQLModel, table=True):
    """User model."""
    __tablename__ = "user"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True
    )
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    tags: List["Tag"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class Task(SQLModel, table=True):
    """Task model."""
    __tablename__ = "task"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True
    )
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False, index=True)
    due_date: Optional[datetime] = Field(default=None, index=True)
    priority: Priority = Field(default=Priority.MEDIUM, index=True)
    is_recurring: bool = Field(default=False, index=True)
    recurrence_type: Optional[RecurrenceType] = None
    recurrence_interval: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional[User] = Relationship(back_populates="tasks")
    reminders: List["Reminder"] = Relationship(back_populates="task", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)


class Tag(SQLModel, table=True):
    """Tag model for categorizing tasks."""
    __tablename__ = "tag"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True
    )
    user_id: str = Field(foreign_key="user.id", index=True)
    name: str = Field(index=True)
    color: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional[User] = Relationship(back_populates="tags")
    tasks: List[Task] = Relationship(back_populates="tags", link_model=TaskTag)


class Reminder(SQLModel, table=True):
    """Reminder model for task notifications."""
    __tablename__ = "reminder"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True
    )
    task_id: str = Field(foreign_key="task.id", index=True)
    remind_at: datetime = Field(index=True)
    sent: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    task: Optional[Task] = Relationship(back_populates="reminders")
