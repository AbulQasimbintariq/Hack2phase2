"""
Authentication endpoints for user signup, login, and profile management.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session

from .. import schemas
from ..database import get_db
from ..auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..crud import create_user, authenticate_user, get_user_by_email, get_user_by_id
from ..dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


@router.post("/signup", response_model=schemas.Token)
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.

    - **email**: Valid email address
    - **password**: Strong password (8+ characters)
    - **name**: Optional user name

    Returns JWT access token on success.
    """
    # Check if user already exists
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    db_user = create_user(db, email=user.email, password=user.password, name=user.name)

    # Generate access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.Token)
async def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate an existing user.

    - **email**: Registered email address
    - **password**: User password

    Returns JWT access token on success.
    """
    user = authenticate_user(db, email=credentials.email, password=credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """
    Get the current authenticated user's profile information.

    Requires valid JWT token in Authorization header.
    """
    return current_user
