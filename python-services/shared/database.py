"""
YugabyteDB YSQL connection pooling and SQLModel base configuration.

Provides async database connection management for Bookstore-R-Us Python services.
Uses SQLModel (combines SQLAlchemy + Pydantic) for type-safe ORM operations.

Features:
- Async connection pooling (asyncpg driver)
- PostgreSQL-compatible (YSQL)
- Type-safe models with Pydantic validation
- Automatic connection lifecycle management
- Health check support

Connection String Format:
    postgresql+asyncpg://user:password@host:port/database
"""

from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool, QueuePool
from sqlmodel import SQLModel
import os
from contextlib import asynccontextmanager


# Database configuration from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://yugabyte:yugabyte@localhost:5433/yugabyte"
)

# Connection pool configuration
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "20"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
POOL_PRE_PING = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"
POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "3600"))  # 1 hour
ECHO_SQL = os.getenv("DB_ECHO_SQL", "false").lower() == "true"


# Global engine and session maker
_engine = None
_session_maker = None


def get_engine():
    """
    Get or create the database engine.
    
    Singleton pattern - creates engine once and reuses it.
    
    Returns:
        AsyncEngine instance
    
    Configuration:
        - pool_size: Maximum connections in pool (default 20)
        - max_overflow: Additional connections beyond pool_size (default 10)
        - pool_pre_ping: Test connections before using (prevents stale connections)
        - pool_recycle: Recycle connections after N seconds (prevents timeout)
    """
    global _engine
    
    if _engine is None:
        _engine = create_async_engine(
            DATABASE_URL,
            echo=ECHO_SQL,  # Log all SQL statements (useful for debugging)
            poolclass=QueuePool,
            pool_size=POOL_SIZE,
            max_overflow=MAX_OVERFLOW,
            pool_pre_ping=POOL_PRE_PING,
            pool_recycle=POOL_RECYCLE,
        )
    
    return _engine


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    """
    Get or create the session maker.
    
    Returns:
        Async session maker factory
    
    Usage:
        async with get_session_maker()() as session:
            result = await session.execute(select(Product))
            products = result.scalars().all()
    """
    global _session_maker
    
    if _session_maker is None:
        engine = get_engine()
        _session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,  # Don't expire objects after commit
            autocommit=False,
            autoflush=False,
        )
    
    return _session_maker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for getting a database session.
    
    Automatically handles session lifecycle:
    - Creates session
    - Yields session for use in route
    - Commits on success
    - Rolls back on error
    - Closes session

    Usage in FastAPI:
        from fastapi import Depends
        from shared.database import get_session
        
        @app.get("/products")
        async def list_products(session: AsyncSession = Depends(get_session)):
            result = await session.execute(select(Product))
            return result.scalars().all()
    
    Yields:
        AsyncSession instance
    """
    session_maker = get_session_maker()
    
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize database tables.
    
    Creates all tables defined in SQLModel models.
    Should be called on application startup.
    
    Usage:
        from fastapi import FastAPI
        from shared.database import init_db
        
        @app.on_event("startup")
        async def startup():
            await init_db()
    
    Note:
        In production, use migrations instead of create_all()
    """
    engine = get_engine()
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)


async def check_db_health() -> bool:
    """
    Check database connection health.
    
    Useful for health check endpoints.
    
    Returns:
        True if database is accessible, False otherwise
    
    Usage:
        @app.get("/health")
        async def health_check():
            db_healthy = await check_db_health()
            if not db_healthy:
                raise HTTPException(status_code=503, detail="Database unavailable")
            return {"status": "healthy"}
    """
    try:
        session_maker = get_session_maker()
        async with session_maker() as session:
            # Simple query to test connection
            await session.execute("SELECT 1")
            return True
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False


async def close_db():
    """
    Close database connections gracefully.
    
    Should be called on application shutdown.
    
    Usage:
        from fastapi import FastAPI
        from shared.database import close_db
        
        @app.on_event("shutdown")
        async def shutdown():
            await close_db()
    """
    global _engine, _session_maker
    
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_maker = None


# Context manager for manual transaction control
@asynccontextmanager
async def transaction():
    """
    Context manager for manual transaction control.
    
    Use when you need explicit control over transactions
    (e.g., multiple operations that must succeed or fail together).
    
    Usage:
        from shared.database import transaction
        
        async with transaction() as session:
            # Create product
            product = Product(asin="B001", title="Book", price=19.99)
            session.add(product)
            
            # Create metadata
            metadata = ProductMetadata(asin="B001", category="Books")
            session.add(metadata)
            
            # Both committed together or rolled back on error
    
    Yields:
        AsyncSession with transaction
    """
    session_maker = get_session_maker()
    
    async with session_maker() as session:
        async with session.begin():
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


# Base class for all database models
class BaseModel(SQLModel):
    """
    Base class for all database models.
    
    Provides common functionality and configuration.
    
    Usage:
        from shared.database import BaseModel
        from sqlmodel import Field
        
        class Product(BaseModel, table=True):
            __tablename__ = "products"
            
            asin: str = Field(primary_key=True)
            title: str
            price: float
    """
    
    class Config:
        # Enable attribute validation
        validate_assignment = True
        # Use enum values
        use_enum_values = True
        # Arbitrary types allowed (for custom types)
        arbitrary_types_allowed = True


# For testing
if __name__ == "__main__":
    import asyncio
    
    async def test_database():
        print("YugabyteDB Connection Pool Demo")
        print("=" * 50)
        
        # Initialize database
        print("\n1. Initializing database...")
        await init_db()
        print("   ✅ Database initialized")
        
        # Health check
        print("\n2. Checking database health...")
        is_healthy = await check_db_health()
        print(f"   {'✅' if is_healthy else '❌'} Database health: {is_healthy}")
        
        # Get session
        print("\n3. Testing session creation...")
        session_maker = get_session_maker()
        async with session_maker() as session:
            result = await session.execute("SELECT 1 as test")
            value = result.scalar()
            print(f"   ✅ Query result: {value}")
        
        # Close connections
        print("\n4. Closing database connections...")
        await close_db()
        print("   ✅ Connections closed")
        
        print("\n✅ Database utilities working correctly!")
    
    # Run test
    asyncio.run(test_database())
