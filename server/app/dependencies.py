"""
FastAPI dependencies for authentication and database.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session

from .database import get_db
from .auth import verify_token
from .crud import get_user_by_id
from .models import User


# Security scheme for JWT tokens
security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Extract and validate user ID from JWT token.
    Returns user_id if token is valid.
    Raises HTTPException if token is invalid or expired.
    """
    token = credentials.credentials
    user_id = verify_token(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from database.
    Raises HTTPException if user not found.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_optional_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        security if False else lambda: None
    )
) -> Optional[str]:
    """
    Optional authentication - returns user_id if token provided and valid.
    Returns None if no token or invalid token.
    """
    if not credentials:
        return None

    try:
        return await get_current_user_id(credentials)
    except HTTPException:
        return None
