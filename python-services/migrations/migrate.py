"""
Database migration framework for Bookstore-R-Us Python services.

Simple, explicit migration system for managing database schema changes.
Each migration is a numbered Python script with up() and down() functions.

Migration Naming Convention:
    001_initial_schema.py
    002_add_user_roles.py
    003_create_cart_tables.py

Features:
- Explicit migration order (numbered files)
- Rollback support (down migrations)
- Migration history tracking
- Idempotent (safe to run multiple times)
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple
import asyncio
from sqlalchemy import text
from shared.database import get_engine, get_session_maker


# Migration directory
MIGRATIONS_DIR = Path(__file__).parent


class MigrationError(Exception):
    """Raised when migration fails."""
    pass


async def create_migrations_table():
    """
    Create migrations tracking table if it doesn't exist.
    
    Table: migrations_history
    Columns:
        - id: Auto-increment primary key
        - migration: Migration name (e.g., "001_initial_schema")
        - applied_at: Timestamp when migration was applied
    """
    session_maker = get_session_maker()
    
    async with session_maker() as session:
        await session.execute(text("""
            CREATE TABLE IF NOT EXISTS migrations_history (
                id SERIAL PRIMARY KEY,
                migration VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        await session.commit()


async def get_applied_migrations() -> List[str]:
    """
    Get list of already applied migrations.
    
    Returns:
        List of migration names (e.g., ["001_initial_schema", "002_add_users"])
    """
    await create_migrations_table()
    
    session_maker = get_session_maker()
    
    async with session_maker() as session:
        result = await session.execute(
            text("SELECT migration FROM migrations_history ORDER BY id")
        )
        return [row[0] for row in result.fetchall()]


async def mark_migration_applied(migration_name: str):
    """
    Mark a migration as applied in the history table.
    
    Args:
        migration_name: Name of the migration (e.g., "001_initial_schema")
    """
    session_maker = get_session_maker()
    
    async with session_maker() as session:
        await session.execute(
            text("INSERT INTO migrations_history (migration) VALUES (:migration)"),
            {"migration": migration_name}
        )
        await session.commit()


async def unmark_migration(migration_name: str):
    """
    Remove a migration from the history table (for rollback).
    
    Args:
        migration_name: Name of the migration to remove
    """
    session_maker = get_session_maker()
    
    async with session_maker() as session:
        await session.execute(
            text("DELETE FROM migrations_history WHERE migration = :migration"),
            {"migration": migration_name}
        )
        await session.commit()


def get_migration_files() -> List[Tuple[str, Path]]:
    """
    Get all migration files in order.
    
    Returns:
        List of tuples (migration_name, file_path)
        Sorted by migration number
    
    Example:
        [
            ("001_initial_schema", Path(".../001_initial_schema.py")),
            ("002_add_users", Path(".../002_add_users.py"))
        ]
    """
    migrations = []
    
    for file_path in MIGRATIONS_DIR.glob("[0-9][0-9][0-9]_*.py"):
        migration_name = file_path.stem  # Remove .py extension
        migrations.append((migration_name, file_path))
    
    # Sort by migration number
    migrations.sort(key=lambda x: x[0])
    
    return migrations


async def run_migrations(target: str = None):
    """
    Run pending migrations.
    
    Args:
        target: Specific migration to run up to (optional)
                If None, runs all pending migrations
    
    Example:
        # Run all pending migrations
        await run_migrations()
        
        # Run up to specific migration
        await run_migrations(target="002_add_users")
    
    Raises:
        MigrationError: If migration fails
    """
    print("=" * 60)
    print("RUNNING DATABASE MIGRATIONS")
    print("=" * 60)
    
    # Get applied and available migrations
    applied = await get_applied_migrations()
    all_migrations = get_migration_files()
    
    print(f"\nApplied migrations: {len(applied)}")
    print(f"Available migrations: {len(all_migrations)}")
    
    # Find pending migrations
    pending = [
        (name, path) for name, path in all_migrations
        if name not in applied
    ]
    
    if not pending:
        print("\n✅ No pending migrations")
        return
    
    print(f"\nPending migrations: {len(pending)}")
    for name, _ in pending:
        print(f"  - {name}")
    
    # Run each pending migration
    for migration_name, migration_path in pending:
        # Check if we've reached the target
        if target and migration_name > target:
            print(f"\n⏭️  Stopping at target: {target}")
            break
        
        print(f"\n{'=' * 60}")
        print(f"Applying: {migration_name}")
        print(f"{'=' * 60}")
        
        try:
            # Load migration module
            spec = __import__(f"migrations.{migration_name}", fromlist=['up'])
            
            # Run up() function
            if hasattr(spec, 'up'):
                await spec.up()
            else:
                raise MigrationError(f"Migration {migration_name} missing up() function")
            
            # Mark as applied
            await mark_migration_applied(migration_name)
            
            print(f"✅ Applied: {migration_name}")
        
        except Exception as e:
            print(f"❌ Failed: {migration_name}")
            print(f"Error: {str(e)}")
            raise MigrationError(f"Migration {migration_name} failed: {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("✅ ALL MIGRATIONS COMPLETE")
    print(f"{'=' * 60}\n")


async def rollback_migration(migration_name: str = None):
    """
    Rollback the last migration or a specific migration.
    
    Args:
        migration_name: Specific migration to rollback (optional)
                       If None, rolls back the last applied migration
    
    Example:
        # Rollback last migration
        await rollback_migration()
        
        # Rollback specific migration
        await rollback_migration("002_add_users")
    
    Raises:
        MigrationError: If rollback fails
    """
    print("=" * 60)
    print("ROLLING BACK MIGRATION")
    print("=" * 60)
    
    # Get applied migrations
    applied = await get_applied_migrations()
    
    if not applied:
        print("\n❌ No migrations to rollback")
        return
    
    # Determine which migration to rollback
    if migration_name is None:
        migration_name = applied[-1]  # Last applied
    elif migration_name not in applied:
        print(f"\n❌ Migration {migration_name} not applied")
        return
    
    print(f"\nRolling back: {migration_name}")
    
    try:
        # Load migration module
        spec = __import__(f"migrations.{migration_name}", fromlist=['down'])
        
        # Run down() function
        if hasattr(spec, 'down'):
            await spec.down()
        else:
            raise MigrationError(f"Migration {migration_name} missing down() function")
        
        # Remove from history
        await unmark_migration(migration_name)
        
        print(f"✅ Rolled back: {migration_name}")
    
    except Exception as e:
        print(f"❌ Rollback failed: {migration_name}")
        print(f"Error: {str(e)}")
        raise MigrationError(f"Rollback {migration_name} failed: {str(e)}")


async def migration_status():
    """
    Show migration status.
    
    Displays:
    - Applied migrations
    - Pending migrations
    - Total count
    """
    print("=" * 60)
    print("MIGRATION STATUS")
    print("=" * 60)
    
    applied = await get_applied_migrations()
    all_migrations = get_migration_files()
    
    print(f"\nTotal migrations: {len(all_migrations)}")
    print(f"Applied: {len(applied)}")
    print(f"Pending: {len(all_migrations) - len(applied)}")
    
    print("\nApplied Migrations:")
    if applied:
        for migration in applied:
            print(f"  ✅ {migration}")
    else:
        print("  (none)")
    
    print("\nPending Migrations:")
    pending = [name for name, _ in all_migrations if name not in applied]
    if pending:
        for migration in pending:
            print(f"  ⏳ {migration}")
    else:
        print("  (none)")
    
    print()


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database Migration Manager")
    parser.add_argument("command", choices=["up", "down", "status"],
                       help="Migration command")
    parser.add_argument("--target", help="Target migration (for 'up')")
    parser.add_argument("--migration", help="Specific migration (for 'down')")
    
    args = parser.parse_args()
    
    if args.command == "up":
        asyncio.run(run_migrations(target=args.target))
    elif args.command == "down":
        asyncio.run(rollback_migration(migration_name=args.migration))
    elif args.command == "status":
        asyncio.run(migration_status())
