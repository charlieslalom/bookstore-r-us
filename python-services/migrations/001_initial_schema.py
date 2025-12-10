"""
Migration 001: Initial Schema Setup

Creates base tables for migrated services.
"""

from sqlalchemy import text
from shared.database import get_session_maker


async def up():
    """Apply migration: Create initial tables."""
    print("Creating initial schema...")
    
    session_maker = get_session_maker()
    
    async with session_maker() as session:
        # This is a placeholder - actual tables will be created
        # by SQLModel in service-specific migrations
        print("  ✅ Initial schema ready (services will create their own tables)")
        await session.commit()


async def down():
    """Rollback migration: Drop initial tables."""
    print("Rolling back initial schema...")
    
    session_maker = get_session_maker()
    
    async with session_maker() as session:
        # Placeholder for rollback logic
        print("  ✅ Initial schema rollback complete")
        await session.commit()
