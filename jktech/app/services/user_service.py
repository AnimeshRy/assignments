from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import get_password_hash, verify_password
import logging

logger = logging.getLogger(__name__)

class UserService:
    async def create_user(
        self,
        session: AsyncSession,
        username: str,
        email: str,
        password: str,
        is_superuser: bool = False
    ) -> User:
        """Create a new user."""
        hashed_password = get_password_hash(password)
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_superuser=is_superuser
        )
        session.add(user)
        await session.commit()
        return user

    async def get_user(self, session: AsyncSession, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return await session.get(User, user_id)

    async def get_user_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        """Get a user by email."""
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_username(self, session: AsyncSession, username: str) -> Optional[User]:
        """Get a user by username."""
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def authenticate_user(self, session: AsyncSession, username: str, password: str) -> Optional[User]:
        """Authenticate a user."""
        user = await self.get_user_by_username(session, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_superuser: Optional[bool] = None
    ) -> Optional[User]:
        """Update a user."""
        user = await session.get(User, user_id)
        if not user:
            return None

        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if password is not None:
            user.hashed_password = get_password_hash(password)
        if is_active is not None:
            user.is_active = is_active
        if is_superuser is not None:
            user.is_superuser = is_superuser

        await session.commit()
        return user

    async def delete_user(self, session: AsyncSession, user_id: int) -> bool:
        """Delete a user."""
        user = await session.get(User, user_id)
        if not user:
            return False

        await session.delete(user)
        await session.commit()
        return True

    async def get_users(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        stmt = select(User).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()
