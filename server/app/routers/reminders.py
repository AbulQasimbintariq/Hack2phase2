"""
Reminder and automation endpoints for due dates and recurring tasks.
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from sqlmodel import Session


# Fix for FastAPI type annotation conflicts
status = http_status


from .. import schemas
from ..database import get_db
from ..dependencies import get_current_user
from ..crud import (
    get_task_by_id_and_user, update_task,
    get_reminders_by_task, create_reminder, get_user_pending_reminders
)
from ..models import User, RecurrenceType


# User-level reminder endpoints
user_reminders_router = APIRouter(prefix="/reminders", tags=["reminders"])


@user_reminders_router.get("/pending", response_model=list[schemas.ReminderResponse])
async def get_pending_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all pending reminders for the authenticated user.
    """
    reminders = get_user_pending_reminders(db, user_id=str(current_user.id))
    return reminders


# Task-specific reminder endpoints
task_reminders_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_reminders_router.post("/{task_id}/due-date", response_model=schemas.TaskResponse)

from .. import schemas
from ..database import get_db
from ..dependencies import get_current_user
from ..crud import (
    get_task_by_id_and_user, update_task,
    get_reminders_by_task, create_reminder, get_user_pending_reminders
)
from ..models import User, RecurrenceType


# User-level reminder endpoints
user_reminders_router = APIRouter(prefix="/reminders", tags=["reminders"])


@user_reminders_router.get("/pending", response_model=list[schemas.ReminderResponse])
async def get_pending_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all pending reminders for the authenticated user.
    """
    reminders = get_user_pending_reminders(db, user_id=str(current_user.id))
    return reminders


# Task-specific reminder endpoints
task_reminders_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_reminders_router.post("/{task_id}/due-date", response_model=schemas.TaskResponse)
async def set_task_due_date(
    task_id: str,
    due_date_update: schemas.DueDateUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set or update the due date for a task.

    - **due_date**: ISO timestamp (or null to remove due date)
    """
    # Verify task exists and belongs to user
    task = get_task_by_id_and_user(db, task_id=task_id, user_id=str(current_user.id))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )

    # Update due date
    updated_task = update_task(db, task_id=task_id, due_date=due_date_update.due_date)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )

    return updated_task


@task_reminders_router.post("/{task_id}/recurrence", response_model=schemas.TaskResponse)
async def set_task_recurrence(
    task_id: str,
    recurrence_config: schemas.RecurrenceConfig,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Configure task recurrence settings.

    - **recurrence_type**: daily, weekly, or monthly
    - **recurrence_interval**: How often the task recurs
    """
    # Verify task exists and belongs to user
    task = get_task_by_id_and_user(db, task_id=task_id, user_id=str(current_user.id))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )

    # Validate recurrence interval
    if recurrence_config.recurrence_interval <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_SERVER,
            detail="Recurrence interval must be greater than 0"
        )

    # Update task with recurrence settings
    updated_task = update_task(
        db,
        task_id=task_id,
        is_recurring=True,
        recurrence_type=recurrence_config.recurrence_type,
        recurrence_interval=recurrence_config.recurrence_interval
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )

    return updated_task


@task_reminders_router.post("/{task_id}/reminders", response_model=schemas.ReminderResponse)
async def create_task_reminder(
    task_id: str,
    reminder: schemas.ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a reminder for a task.

    - **remind_at**: When to send the reminder (ISO timestamp)
    """
    # Verify task exists and belongs to user
    task = get_task_by_id_and_user(db, task_id=task_id, user_id=str(current_user.id))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )

    # Validate reminder time
    if reminder.remind_at <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reminder time must be in the future"
        )

    # Create reminder
    db_reminder = create_reminder(db, task_id=task_id, remind_at=reminder.remind_at)

    return db_reminder


@task_reminders_router.get("/{task_id}/reminders", response_model=list[schemas.ReminderResponse])
async def get_task_reminders(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all reminders for a specific task.
    """
    # Verify task exists and belongs to user
    task = get_task_by_id_and_user(db, task_id=task_id, user_id=str(current_user.id))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )

    reminders = get_reminders_by_task(db, task_id=task_id)
    return reminders
