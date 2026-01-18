"""
CRUD operations for database models.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import and_, or_
from sqlalchemy.orm import selectinload
from sqlmodel import select, Session

from .models import User, Task, Tag, Reminder, TaskTag, Priority
from .auth import get_password_hash, verify_password


# User CRUD operations
def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """
    Get user by ID.
    """
    return db.exec(select(User).where(User.id == user_id)).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get user by email.
    """
    return db.exec(select(User).where(User.email == email)).first()


def create_user(db: Session, email: str, password: str, name: Optional[str] = None) -> User:
    """
    Create a new user.
    """
    hashed_password = get_password_hash(password)
    db_user = User(email=email, hashed_password=hashed_password, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate user with email and password.
    Returns None if authentication fails.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Tag CRUD operations
def get_user_tag_by_name(db: Session, user_id: str, name: str) -> Optional[Tag]:
    """
    Get a tag by name for a specific user.
    """
    return db.exec(
        select(Tag).where(Tag.user_id == user_id, Tag.name == name)
    ).first()


def get_user_tags(db: Session, user_id: str) -> List[Tag]:
    """
    Get all tags for a user.
    """
    return db.exec(select(Tag).where(Tag.user_id == user_id)).all()


def create_tag(db: Session, user_id: str, name: str, color: Optional[str] = None) -> Tag:
    """
    Create a new tag for a user.
    """
    db_tag = Tag(user_id=user_id, name=name, color=color)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: str) -> bool:
    """
    Delete a tag.
    Returns True if tag was deleted, False if not found.
    """
    tag = db.exec(select(Tag).where(Tag.id == tag_id)).first()
    if not tag:
        return False
    db.delete(tag)
    db.commit()
    return True


# Task CRUD operations
def get_task(db: Session, task_id: str) -> Optional[Task]:
    """
    Get a task by ID with tags loaded.
    """
    return db.exec(
        select(Task).options(selectinload(Task.tags)).where(Task.id == task_id)
    ).first()


def get_user_tasks(
    db: Session,
    user_id: str,
    skip: int = 0,
    limit: int = 100
) -> List[Task]:
    """
    Get all tasks for a user with tags loaded.
    """
    return db.exec(
        select(Task)
        .options(selectinload(Task.tags))
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
    ).all()


def get_task_by_id_and_user(db: Session, task_id: str, user_id: str) -> Optional[Task]:
    """
    Get a task by ID and verify it belongs to the user.
    """
    return db.exec(
        select(Task).options(selectinload(Task.tags)).where(
            Task.id == task_id, Task.user_id == user_id
        )
    ).first()


def create_task(
    db: Session,
    user_id: str,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    priority: Priority = Priority.MEDIUM
) -> Task:
    """
    Create a new task for a user.
    """
    db_task = Task(
        user_id=user_id,
        title=title,
        description=description,
        due_date=due_date,
        priority=priority
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: str, **kwargs) -> Optional[Task]:
    """
    Update a task with the given fields.
    """
    task = get_task(db, task_id)
    if not task:
        return None

    for key, value in kwargs.items():
        if hasattr(task, key) and value is not None:
            setattr(task, key, value)

    task.updated_at = datetime.utcnow()
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: str) -> bool:
    """
    Delete a task and its associated reminders.
    Returns True if task was deleted, False if not found.
    """
    task = db.exec(select(Task).where(Task.id == task_id)).first()
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True


# Task-Tag operations
def add_tag_to_task(db: Session, task_id: str, tag_id: str) -> bool:
    """
    Add a tag to a task.
    Returns True if successful, False if already exists.
    """
    # Check if association already exists
    existing = db.exec(
        select(TaskTag).where(TaskTag.task_id == task_id, TaskTag.tag_id == tag_id)
    ).first()

    if existing:
        return False

    # Create association
    association = TaskTag(task_id=task_id, tag_id=tag_id)
    db.add(association)
    db.commit()
    return True


def remove_tag_from_task(db: Session, task_id: str, tag_id: str) -> bool:
    """
    Remove a tag from a task.
    Returns True if removed, False if not found.
    """
    association = db.exec(
        select(TaskTag).where(TaskTag.task_id == task_id, TaskTag.tag_id == tag_id)
    ).first()

    if not association:
        return False

    db.delete(association)
    db.commit()
    return True


# Task search, filter, and sort operations
def search_user_tasks(db: Session, user_id: str, query: str) -> List[Task]:
    """
    Search tasks by title or description for a specific user.
    """
    search_term = f"%{query.lower()}%"
    return db.exec(
        select(Task)
        .options(selectinload(Task.tags))
        .where(
            Task.user_id == user_id,
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )
        .order_by(Task.created_at.desc())
    ).all()


def filter_user_tasks(
    db: Session,
    user_id: str,
    completed: Optional[bool] = None,
    priority: Optional[Priority] = None,
    tag: Optional[str] = None,
    due_before: Optional[datetime] = None,
    due_after: Optional[datetime] = None
) -> List[Task]:
    """
    Filter tasks by various criteria for a specific user.
    """
    query = select(Task).options(selectinload(Task.tags)).where(Task.user_id == user_id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    if priority is not None:
        query = query.where(Task.priority == priority)

    if tag is not None:
        # Filter by tag name
        query = query.join(Task.tags).where(Tag.name == tag)

    if due_before is not None:
        query = query.where(Task.due_date <= due_before)

    if due_after is not None:
        query = query.where(Task.due_date >= due_after)

    return db.exec(query.order_by(Task.created_at.desc())).all()


def sort_user_tasks(
    db: Session,
    user_id: str,
    sort_by: str = "created_at",
    order: str = "desc"
) -> List[Task]:
    """
    Sort tasks by specified field and order for a user.
    """
    # Map sort_by to actual column
    sort_column = {
        "created_at": Task.created_at,
        "due_date": Task.due_date,
        "priority": Task.priority,
        "title": Task.title
    }.get(sort_by, Task.created_at)

    # Apply sort order
    if order.lower() == "asc":
        query = select(Task).options(selectinload(Task.tags)).where(
            Task.user_id == user_id
        ).order_by(sort_column.asc())
    else:
        query = select(Task).options(selectinload(Task.tags)).where(
            Task.user_id == user_id
        ).order_by(sort_column.desc())

    return db.exec(query).all()


# Reminder CRUD operations
def get_reminder(db: Session, reminder_id: str) -> Optional[Reminder]:
    """
    Get a reminder by ID.
    """
    return db.exec(select(Reminder).where(Reminder.id == reminder_id)).first()


def get_user_pending_reminders(db: Session, user_id: str) -> List[Reminder]:
    """
    Get all pending reminders for a user's tasks.
    """
    return db.exec(
        select(Reminder)
        .join(Task)
        .where(
            Task.user_id == user_id,
            Reminder.sent == False,
            Reminder.remind_at <= datetime.utcnow()
        )
        .order_by(Reminder.remind_at.asc())
    ).all()


def get_reminders_by_task(db: Session, task_id: str) -> List[Reminder]:
    """
    Get all reminders for a task.
    """
    return db.exec(
        select(Reminder).where(Reminder.task_id == task_id).order_by(Reminder.remind_at.asc())
    ).all()


def create_reminder(db: Session, task_id: str, remind_at: datetime) -> Reminder:
    """
    Create a new reminder for a task.
    """
    db_reminder = Reminder(task_id=task_id, remind_at=remind_at)
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


def mark_reminder_sent(db: Session, reminder_id: str) -> bool:
    """
    Mark a reminder as sent.
    Returns True if updated, False if not found.
    """
    reminder = db.exec(select(Reminder).where(Reminder.id == reminder_id)).first()
    if not reminder:
        return False

    reminder.sent = True
    db.add(reminder)
    db.commit()
    return True


# Recurring task operations
def get_completed_recurring_tasks(db: Session) -> List[Task]:
    """
    Get all completed recurring tasks that are due for regeneration.
    """
    return db.exec(
        select(Task)
        .where(
            Task.is_recurring == True,
            Task.completed == True,
            Task.due_date.isnot(None),
            Task.due_date < datetime.utcnow()
        )
    ).all()


def create_next_recurring_task(db: Session, task: Task) -> Optional[Task]:
    """
    Create the next instance of a recurring task.
    """
    if not task.is_recurring or not task.recurrence_type or not task.due_date:
        return None

    # Calculate next due date
    from datetime import timedelta
    import calendar

    if task.recurrence_type.value == "daily":
        next_due = task.due_date + timedelta(days=task.recurrence_interval or 1)
    elif task.recurrence_type.value == "weekly":
        next_due = task.due_date + timedelta(weeks=task.recurrence_interval or 1)
    elif task.recurrence_type.value == "monthly":
        # Add months (approximation)
        month = task.due_date.month - 1 + (task.recurrence_interval or 1)
        year = task.due_date.year + month // 12
        month = month % 12 + 1
        day = min(task.due_date.day, calendar.monthrange(year, month)[1])
        next_due = task.due_date.replace(year=year, month=month, day=day)
    else:
        return None

    # Create new task instance
    new_task = Task(
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        due_date=next_due,
        priority=task.priority,
        is_recurring=True,
        recurrence_type=task.recurrence_type,
        recurrence_interval=task.recurrence_interval,
        completed=False
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
