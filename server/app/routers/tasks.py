"""
Task CRUD endpoints and task organization endpoints.
"""

from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from .. import schemas
from ..database import get_db
from ..dependencies import get_current_user, get_current_user_id
from ..crud import (
    create_task, get_task, get_user_tasks, get_task_by_id_and_user,
    update_task, delete_task,
    search_user_tasks, filter_user_tasks, sort_user_tasks,
    add_tag_to_task, remove_tag_from_task, get_user_tag_by_name, create_tag
)
from ..models import User, Tag

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=schemas.TaskResponse)
async def create_new_task(
    task: schemas.TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user.

    - **title**: Task title (required)
    - **description**: Optional task description
    - **completed**: Initial completion status
    - **due_date**: Optional due date (ISO timestamp)
    - **priority**: Priority level (low/medium/high)
    - **is_recurring**: Whether task recurs
    - **recurrence_type**: daily/weekly/monthly
    - **recurrence_interval**: Recurrence interval
    """
    if not task.title or not task.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title is required"
        )

    db_task = create_task(
        db,
        user_id=str(current_user.id),
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        priority=task.priority
    )

    return db_task


@router.get("", response_model=list[schemas.TaskResponse])
async def list_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Get all tasks for the authenticated user with pagination.
    """
    tasks = get_user_tasks(db, user_id=str(current_user.id), skip=skip, limit=limit)
    return tasks


@router.get("/{task_id}", response_model=schemas.TaskResponse)
async def get_task_detail(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID.
    """
    task = get_task_by_id_and_user(db, task_id=task_id, user_id=str(current_user.id))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )
    return task


@router.put("/{task_id}", response_model=schemas.TaskResponse)
async def update_task_endpoint(
    task_id: str,
    task_update: schemas.TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing task (partial updates supported).

    Any field can be updated. Fields not provided remain unchanged.
    """
    # Verify task exists and belongs to user
    existing_task = get_task_by_id_and_user(db, task_id=task_id, user_id=str(current_user.id))
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )

    # Title validation if provided
    if task_update.title is not None and (not task_update.title or not task_update.title.strip()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty"
        )

    # Update task
    kwargs = task_update.model_dump(exclude_unset=True)
    updated_task = update_task(db, task_id=task_id, **kwargs)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )

    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a task and all its associated reminders.
    """
    # Verify task exists and belongs to user
    task = get_task_by_id_and_user(db, task_id=task_id, user_id=str(current_user.id))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )

    if not delete_task(db, task_id=task_id):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )

    return None


# Task Organization Endpoints

@router.get("/search", response_model=list[schemas.TaskResponse])
async def search_tasks(
    q: str = Query(..., description="Search query for title or description"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search tasks by keyword in title or description.

    - **q**: Search query string
    """
    if not q or not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query cannot be empty"
        )

    tasks = search_user_tasks(db, user_id=str(current_user.id), query=q)
    return tasks


@router.get("/filter", response_model=list[schemas.TaskResponse])
async def filter_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, description="Filter by priority (low/medium/high)"),
    tag: Optional[str] = Query(None, description="Filter by tag name"),
    due_before: Optional[datetime] = Query(None, description="Due before date (ISO timestamp)"),
    due_after: Optional[datetime] = Query(None, description="Due after date (ISO timestamp)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Filter tasks by various criteria.

    Multiple filters can be combined.
    """
    # Validate priority if provided
    if priority and priority not in ["low", "medium", "high"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid priority value. Must be low, medium, or high"
        )

    tasks = filter_user_tasks(
        db,
        user_id=str(current_user.id),
        completed=completed,
        priority=priority,
        tag=tag,
        due_before=due_before,
        due_after=due_after
    )
    return tasks


@router.get("/sort", response_model=list[schemas.TaskResponse])
async def sort_tasks(
    by: str = Query("created_at", description="Sort by field: due_date, priority, title, created_at"),
    order: str = Query("desc", description="Sort order: asc or desc"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Sort tasks by specified field and order.

    - **by**: Field to sort by
    - **order**: Sort order (asc/desc)
    """
    # Validate sort_by parameter
    valid_sort_fields = ["due_date", "priority", "title", "created_at"]
    if by not in valid_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort field. Must be one of: {', '.join(valid_sort_fields)}"
        )

    # Validate order parameter
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order. Must be asc or desc"
        )

    tasks = sort_user_tasks(
        db,
        user_id=str(current_user.id),
        sort_by=by,
        order=order
    )
    return tasks


# Tag operations for tasks

@router.post("/{task_id}/tags/{tag_name}", response_model=schemas.TaskResponse)
async def add_tag_to_task_endpoint(
    task_id: str,
    tag_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a tag to a task. Creates the tag if it doesn't exist.
    """
    # Verify task exists and belongs to user
    task = get_task_by_id_and_user(db, task_id=task_id, user_id=str(current_user.id))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )

    # Get or create tag
    tag = get_user_tag_by_name(db, user_id=str(current_user.id), name=tag_name)
    if not tag:
        tag = create_tag(db, user_id=str(current_user.id), name=tag_name)

    # Add tag to task
    if not add_tag_to_task(db, task_id=task_id, tag_id=tag.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag is already assigned to this task"
        )

    # Return updated task
    updated_task = get_task(db, task_id=task_id)
    return updated_task


@router.delete("/{task_id}/tags/{tag_name}", response_model=schemas.TaskResponse)
async def remove_tag_from_task_endpoint(
    task_id: str,
    tag_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a tag from a task.
    """
    # Verify task exists and belongs to user
    task = get_task_by_id_and_user(db, task_id=task_id, user_id=str(current_user.id))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )

    # Get tag
    tag = get_user_tag_by_name(db, user_id=str(current_user.id), name=tag_name)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )

    # Remove tag from task
    if not remove_tag_from_task(db, task_id=task_id, tag_id=tag.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag is not assigned to this task"
        )

    # Return updated task
    updated_task = get_task(db, task_id=task_id)
    return updated_task
