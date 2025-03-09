from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, User as UserSchema
from app.services.user_service import UserService
from app.api.deps import get_current_user, get_current_active_superuser

router = APIRouter()

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    session: AsyncSession = Depends(get_async_session),
    user_in: UserCreate,
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """Create new user (superuser only)."""
    user_service = UserService()

    # Check if user with this email or username already exists
    user = await user_service.get_user_by_email(session, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists."
        )

    user = await user_service.get_user_by_username(session, user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists."
        )

    user = await user_service.create_user(
        session=session,
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
        is_superuser=user_in.is_superuser
    )
    return user

@router.get("/me", response_model=UserSchema)
async def read_user_me(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user."""
    return current_user

@router.put("/me", response_model=UserSchema)
async def update_user_me(
    *,
    session: AsyncSession = Depends(get_async_session),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Update current user."""
    user_service = UserService()

    # Check if email is being changed and if it's already taken
    if user_in.email and user_in.email != current_user.email:
        user = await user_service.get_user_by_email(session, user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="A user with this email already exists."
            )

    # Check if username is being changed and if it's already taken
    if user_in.username and user_in.username != current_user.username:
        user = await user_service.get_user_by_username(session, user_in.username)
        if user:
            raise HTTPException(
                status_code=400,
                detail="A user with this username already exists."
            )

    user = await user_service.update_user(
        session=session,
        user_id=current_user.id,
        username=user_in.username,
        email=user_in.email,
        password=user_in.password
    )
    return user

@router.get("/{user_id}", response_model=UserSchema)
async def read_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """Get a specific user by id (superuser only)."""
    user_service = UserService()
    user = await user_service.get_user(session, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user

@router.get("/", response_model=List[UserSchema])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """Retrieve users (superuser only)."""
    user_service = UserService()
    users = await user_service.get_users(session, skip=skip, limit=limit)
    return users
