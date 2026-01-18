"""
Pydantic schemas for API request/response validation.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from .models import Priority, RecurrenceType


# User schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str


class UserResponse(UserBase):
    """Response schema for user."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


# Auth response schemas
class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    user_id: str


# Tag schemas
class TagBase(BaseModel):
    """Base tag schema."""
    name: str
    color: Optional[str] = None


class TagCreate(TagBase):
    """Schema for tag creation."""
    pass


class TagResponse(TagBase):
    """Response schema for tag."""
    id: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# Task schemas
class TaskBase(BaseModel):
    """Base task schema."""
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[datetime] = None
    priority: Priority = Priority.MEDIUM
    is_recurring: bool = False
    recurrence_type: Optional[RecurrenceType] = None
    recurrence_interval: Optional[int] = None


class TaskCreate(TaskBase):
    """Schema for task creation."""
    pass


class TaskUpdate(BaseModel):
    """Schema for task update (partial updates)."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None
    is_recurring: Optional[bool] = None
    recurrence_type: Optional[RecurrenceType] = None
    recurrence_interval: Optional[int] = None


class TaskResponse(TaskBase):
    """Response schema for task."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    tags: Optional[List[TagResponse]] = None

    class Config:
        from_attributes = True


# Reminder schemas
class ReminderBase(BaseModel):
    """Base reminder schema."""
    remind_at: datetime


class ReminderCreate(ReminderBase):
    """Schema for reminder creation."""
    pass


class ReminderResponse(ReminderBase):
    """Response schema for reminder."""
    id: str
    task_id: str
    sent: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Query parameter schemas
class TaskFilters(BaseModel):
    """Query parameters for filtering tasks."""
    completed: Optional[bool] = None
    priority: Optional[Priority] = None
    tag: Optional[str] = None
    due_before: Optional[datetime] = None
    due_after: Optional[datetime] = None


class SortOptions(BaseModel):
    """Query parameters for sorting tasks."""
    by: str = "created_at"  # due_date | priority | title | created_at
    order: str = "desc"  # asc | desc


# Automation schemas
class DueDateUpdate(BaseModel):
    """Schema for updating task due date."""
    due_date: Optional[datetime] = None


class RecurrenceConfig(BaseModel):
    """Schema for configuring task recurrence."""
    recurrence_type: RecurrenceType
    recurrence_interval: int


# Search schema
class SearchQuery(BaseModel):
    """Schema for search query."""
    q: str
