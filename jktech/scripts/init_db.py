#!/usr/bin/env python3
"""
Script to initialize the database with tables and initial data.
This script runs the Alembic migrations and creates a superuser.
"""

import asyncio
import os
import sys
from pathlib import Path
import subprocess

# Add the parent directory to the path so we can import the app
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_async_session
from app.services.user_service import UserService

async def create_superuser():
    """Create a superuser if one doesn't exist."""
    async for session in get_async_session():
        try:
            user_service = UserService()

            # Check if a superuser already exists
            admin = await user_service.get_user_by_username(session, "admin")
            if admin:
                print("Superuser 'admin' already exists.")
                return

            # Create a superuser
            admin = await user_service.create_user(
                session=session,
                username="admin",
                email="admin@example.com",
                password="adminpass123",  # In production, use a secure password
                is_superuser=True
            )
            print(f"Created superuser: {admin.username} (ID: {admin.id})")

        except Exception as e:
            print(f"Error creating superuser: {str(e)}")
            raise

def run_migrations():
    """Run Alembic migrations to create database tables."""
    try:
        print("Running database migrations...")
        result = subprocess.run(["alembic", "upgrade", "head"], check=True)
        if result.returncode == 0:
            print("Migrations completed successfully.")
        else:
            print("Migrations failed.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {str(e)}")
        sys.exit(1)
    except FileNotFoundError:
        print("Alembic command not found. Make sure it's installed.")
        sys.exit(1)

async def main():
    """Initialize the database."""
    # Run migrations
    run_migrations()

    # Create superuser
    await create_superuser()

    print("Database initialization complete!")

if __name__ == "__main__":
    asyncio.run(main())
