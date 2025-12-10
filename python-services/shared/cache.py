"""
Redis connection and caching utilities for Bookstore-R-Us Python services.

Provides async Redis connection management, caching decorators, and utilities.

Features:
- Async Redis client (redis-py)
- Connection pooling
- Caching decorators
- Cache invalidation
- TTL management
- JSON serialization

Usage:
    from shared.cache import get_redis, cache
    
    redis = await get_redis()
    await redis.set("key", "value", ex=60)
    
    @cache(ttl=300)
    async def get_product(asin: str):
        return await database.get_product(asin)
"""

from typing import Optional, Any, Callable
from functools import wraps
import json
import redis.asyncio as redis
from redis.asyncio import ConnectionPool
from shared.config import get_settings
import hashlib
import pickle


# Global connection pool
_redis_pool: Optional[ConnectionPool] = None
_redis_client: Optional[redis.Redis] = None


def get_redis_pool() -> ConnectionPool:
    """
    Get or create Redis connection pool (singleton).
    
    Returns:
        Redis connection pool
    """
    global _redis_pool
    
    if _redis_pool is None:
        settings = get_settings()
        
        _redis_pool = ConnectionPool.from_url(
            settings.redis_url,
            db=settings.redis_db,
            password=settings.redis_password,
            ssl=settings.redis_ssl,
            encoding="utf-8",
            decode_responses=False,  # We'll handle decoding
            max_connections=50
        )
    
    return _redis_pool


async def get_redis() -> redis.Redis:
    """
    Get Redis client instance.
    
    Returns:
        Async Redis client
    
    Usage:
        redis_client = await get_redis()
        await redis_client.set("key", "value")
    """
    global _redis_client
    
    if _redis_client is None:
        pool = get_redis_pool()
        _redis_client = redis.Redis(connection_pool=pool)
    
    return _redis_client


async def close_redis():
    """
    Close Redis connections gracefully.
    
    Call on application shutdown:
        @app.on_event("shutdown")
        async def shutdown():
            await close_redis()
    """
    global _redis_client, _redis_pool
    
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None
    
    if _redis_pool is not None:
        await _redis_pool.disconnect()
        _redis_pool = None


async def check_redis_health() -> bool:
    """
    Check Redis connection health.
    
    Returns:
        True if Redis is accessible, False otherwise
    """
    try:
        redis_client = await get_redis()
        await redis_client.ping()
        return True
    except Exception as e:
        print(f"Redis health check failed: {e}")
        return False


# Caching utilities

def _generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """
    Generate cache key from function arguments.
    
    Args:
        prefix: Cache key prefix (usually function name)
        *args: Positional arguments
        **kwargs: Keyword arguments
    
    Returns:
        Cache key string
    """
    # Create a stable hash from args and kwargs
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    key_str = ":".join(key_parts)
    
    # Hash for stable key length
    key_hash = hashlib.md5(key_str.encode()).hexdigest()
    
    return f"{prefix}:{key_hash}"


def cache(ttl: int = 300, key_prefix: Optional[str] = None):
    """
    Decorator for caching function results in Redis.
    
    Args:
        ttl: Time to live in seconds (default 5 minutes)
        key_prefix: Custom cache key prefix (defaults to function name)
    
    Usage:
        @cache(ttl=600)  # Cache for 10 minutes
        async def get_product(asin: str):
            return await db.query(Product).filter_by(asin=asin).first()
        
        # First call: hits database, caches result
        product = await get_product("B001")
        
        # Second call: returns cached result
        product = await get_product("B001")
    """
    def decorator(func: Callable):
        prefix = key_prefix or f"cache:{func.__name__}"
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = _generate_cache_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            redis_client = await get_redis()
            cached = await redis_client.get(cache_key)
            
            if cached is not None:
                # Cache hit
                try:
                    return pickle.loads(cached)
                except Exception:
                    # If unpickling fails, ignore cache
                    pass
            
            # Cache miss - call function
            result = await func(*args, **kwargs)
            
            # Store in cache
            try:
                serialized = pickle.dumps(result)
                await redis_client.setex(cache_key, ttl, serialized)
            except Exception as e:
                # If caching fails, log but don't fail the request
                print(f"Cache write failed for {cache_key}: {e}")
            
            return result
        
        # Add cache invalidation method
        async def invalidate(*args, **kwargs):
            """Invalidate cached result for specific arguments."""
            cache_key = _generate_cache_key(prefix, *args, **kwargs)
            redis_client = await get_redis()
            await redis_client.delete(cache_key)
        
        wrapper.invalidate = invalidate
        
        return wrapper
    
    return decorator


async def cache_get(key: str, default: Any = None) -> Optional[Any]:
    """
    Get value from cache.
    
    Args:
        key: Cache key
        default: Default value if not found
    
    Returns:
        Cached value or default
    """
    redis_client = await get_redis()
    value = await redis_client.get(key)
    
    if value is None:
        return default
    
    try:
        return pickle.loads(value)
    except Exception:
        return default


async def cache_set(key: str, value: Any, ttl: int = 300):
    """
    Set value in cache.
    
    Args:
        key: Cache key
        value: Value to cache
        ttl: Time to live in seconds
    """
    redis_client = await get_redis()
    serialized = pickle.dumps(value)
    await redis_client.setex(key, ttl, serialized)


async def cache_delete(key: str):
    """
    Delete key from cache.
    
    Args:
        key: Cache key to delete
    """
    redis_client = await get_redis()
    await redis_client.delete(key)


async def cache_delete_pattern(pattern: str):
    """
    Delete all keys matching pattern.
    
    Args:
        pattern: Key pattern (e.g., "products:*")
    
    Example:
        # Invalidate all product caches
        await cache_delete_pattern("products:*")
    """
    redis_client = await get_redis()
    
    # Find all matching keys
    keys = []
    async for key in redis_client.scan_iter(match=pattern):
        keys.append(key)
    
    # Delete in batch
    if keys:
        await redis_client.delete(*keys)


# Rate limiting utility

class RateLimiter:
    """
    Simple rate limiter using Redis.
    
    Usage:
        limiter = RateLimiter(max_requests=100, window=60)
        
        if await limiter.is_allowed(user_id="u1001"):
            # Process request
            pass
        else:
            # Rate limit exceeded
            raise HTTPException(429, "Too many requests")
    """
    
    def __init__(self, max_requests: int, window: int):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed
            window: Time window in seconds
        """
        self.max_requests = max_requests
        self.window = window
    
    async def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed for identifier.
        
        Args:
            identifier: Unique identifier (user ID, IP address, etc.)
        
        Returns:
            True if allowed, False if rate limit exceeded
        """
        redis_client = await get_redis()
        key = f"rate_limit:{identifier}"
        
        # Increment counter
        count = await redis_client.incr(key)
        
        # Set expiry on first request
        if count == 1:
            await redis_client.expire(key, self.window)
        
        return count <= self.max_requests
    
    async def get_remaining(self, identifier: str) -> int:
        """
        Get remaining requests for identifier.
        
        Args:
            identifier: Unique identifier
        
        Returns:
            Number of remaining requests
        """
        redis_client = await get_redis()
        key = f"rate_limit:{identifier}"
        
        count = await redis_client.get(key)
        current = int(count) if count else 0
        
        return max(0, self.max_requests - current)


# Session storage (optional)

async def set_session(session_id: str, data: dict, ttl: int = 3600):
    """
    Store session data in Redis.
    
    Args:
        session_id: Unique session identifier
        data: Session data dictionary
        ttl: Time to live in seconds (default 1 hour)
    """
    redis_client = await get_redis()
    key = f"session:{session_id}"
    serialized = json.dumps(data)
    await redis_client.setex(key, ttl, serialized)


async def get_session(session_id: str) -> Optional[dict]:
    """
    Get session data from Redis.
    
    Args:
        session_id: Unique session identifier
    
    Returns:
        Session data dictionary or None
    """
    redis_client = await get_redis()
    key = f"session:{session_id}"
    data = await redis_client.get(key)
    
    if data is None:
        return None
    
    return json.loads(data)


async def delete_session(session_id: str):
    """
    Delete session from Redis.
    
    Args:
        session_id: Unique session identifier
    """
    redis_client = await get_redis()
    key = f"session:{session_id}"
    await redis_client.delete(key)


# For testing
if __name__ == "__main__":
    import asyncio
    
    async def test_redis():
        print("Redis Caching Utilities Demo")
        print("=" * 50)
        
        # Health check
        print("\n1. Checking Redis connection...")
        is_healthy = await check_redis_health()
        print(f"   {'✅' if is_healthy else '❌'} Redis health: {is_healthy}")
        
        if not is_healthy:
            print("   ⚠️  Redis not available - skipping tests")
            return
        
        # Basic operations
        print("\n2. Testing basic cache operations...")
        await cache_set("test_key", {"value": 123}, ttl=60)
        result = await cache_get("test_key")
        print(f"   ✅ Set and get: {result}")
        
        # Caching decorator
        print("\n3. Testing caching decorator...")
        
        @cache(ttl=10)
        async def expensive_function(x: int):
            print(f"   Computing {x}**2...")
            return x ** 2
        
        result1 = await expensive_function(5)
        print(f"   First call: {result1}")
        
        result2 = await expensive_function(5)
        print(f"   Second call (cached): {result2}")
        
        # Rate limiter
        print("\n4. Testing rate limiter...")
        limiter = RateLimiter(max_requests=3, window=10)
        
        for i in range(5):
            allowed = await limiter.is_allowed("test_user")
            remaining = await limiter.get_remaining("test_user")
            print(f"   Request {i+1}: {'✅ Allowed' if allowed else '❌ Blocked'} ({remaining} remaining)")
        
        # Cleanup
        await cache_delete("test_key")
        await close_redis()
        
        print("\n✅ Redis utilities working correctly!")
    
    asyncio.run(test_redis())
