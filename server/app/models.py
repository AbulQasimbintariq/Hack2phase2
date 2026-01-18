"""
Database models for the Todo application.
Using SQLModel for Pydantic + SQLAlchemy integration.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import uuid4

from sqlmodel import SQLModel, Field, Relationship, Column, ForeignKey
from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID


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
task_tag = SQLModel.metadata.tables.get('task_tag')
if task_tag is None:
    task_tag = SQLModel.metadata.tables[
        'task_tag'
    ] = SQLModel.metadata.Table(
        'task_tag',
        SQLModel.metadata,
        Column('task_id', UUID(as_uuid=True), ForeignKey('task.id'), primary_key=True),
        Column('tag_id', UUID(as_uuid=True), ForeignKey('tag.id'), primary_key=True)
    )


class User(SQLModel, table=True):
    """User model."""
    __tablename__ = "user"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(UUID(as_uuid=True), primary_key=True)
    )
    email: str = Field(sa_column=Column(unique=True, index=True))
    name: Optional[str] = None
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)
    tags: List["Tag"] = Relationship(back_populates="user", cascade_delete=True)


class Task(SQLModel, table=True):
    """Task model."""
    __tablename__ = "task"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(UUID(as_uuid=True), primary_key=True)
    )
    user_id: str = Field(
        foreign_key="user.id",
        sa_column=Column(UUID(as_uuid=True), index=True)
    )
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False, sa_column=Column(index=True))
    due_date: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
    priority: Priority = Field(default=Priority.MEDIUM, sa_column=Column(index=True))
    is_recurring: bool = Field(default=False, sa_column=Column(index=True))
    recurrence_type: Optional[RecurrenceType] = None
    recurrence_interval: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )

    # Relationships
    user: Optional[User] = Relationship(back_populates="tasks")
    reminders: List["Reminder"] = Relationship(back_populates="task", cascade_delete=True)
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=task_tag)


class Tag(SQLModel, table=True):
    """Tag model for categorizing tasks."""
    __tablename__ = "tag"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(UUID(as_uuid=True), primary_key=True)
    )
    user_id: str = Field(
        foreign_key="user.id",
        sa_column=Column(UUID(as_uuid=True), index=True)
    )
    name: str = Field(sa_column=Column(index=True))
    color: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))

    # Relationships
    user: Optional[User] = Relationship(back_populates="tags")
    tasks: List[Task] = Relationship(back_populates="tags", link_model=task_tag)


class Reminder(SQLModel, table=True):
    """Reminder model for task notifications."""
    __tablename__ = "reminder"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(UUID(as_uuid=True), primary_key=True)
    )
    task_id: str = Field(
        foreign_key="task.id",
        sa_column=Column(UUID(as_uuid=True), index=True)
    )
    remind_at: datetime = Field(sa_column=Column(DateTime(timezone=True), index=True))
    sent: bool = Field(default=False, sa_column=Column(index=True))
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))

    # Relationships
    task: Optional[Task] = Relationship(back_populates="reminders")


class TaskTag(SQLModel, table=True):
    """Association table for Task-Tag many-to-many relationship."""
    __tablename__ = "task_tag"

    task_id: str = Field(
        foreign_key="task.id",
        sa_column=Column(UUID(as_uuid=True), primary_key=True)
    )
    tag_id: str = Field(
        foreign_key="tag.id",
        sa_column=Column(UUID(as_uuid=True), primary_key=True)
    )
