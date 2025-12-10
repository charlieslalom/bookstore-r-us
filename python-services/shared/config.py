"""
Environment variable configuration management.

Provides centralized configuration loading and validation for Python services.
Uses Pydantic for type validation and environment variable parsing.

Features:
- Type-safe configuration
- Environment variable loading (.env files)
- Default values with overrides
- Validation on startup
- Separate configs per environment (dev, staging, prod)

Usage:
    from shared.config import get_settings
    
    settings = get_settings()
    print(settings.database_url)
    print(settings.jwt_secret_key)
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Environment variables are loaded from:
    1. System environment
    2. .env file (if present)
    
    Override with environment-specific files:
    - .env.development
    - .env.staging
    - .env.production
    """
    
    # Environment
    environment: str = "development"
    debug: bool = False
    
    # Application
    app_name: str = "bookstore-service"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False  # Hot reload (development only)
    
    # Database (YugabyteDB YSQL)
    database_url: str = "postgresql+asyncpg://yugabyte:yugabyte@localhost:5433/yugabyte"
    db_pool_size: int = 20
    db_max_overflow: int = 10
    db_pool_recycle: int = 3600  # 1 hour
    db_pool_pre_ping: bool = True
    db_echo_sql: bool = False
    
    # Redis (Caching)
    redis_url: str = "redis://localhost:6379"
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_ssl: bool = False
    cache_ttl: int = 300  # 5 minutes default
    
    # JWT Authentication
    jwt_secret_key: str = "bookstore-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7
    
    # CORS
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    
    # Service Discovery
    eureka_server_url: Optional[str] = None  # Legacy - will be removed
    products_service_url: str = "http://localhost:8082"
    cart_service_url: str = "http://localhost:8083"
    checkout_service_url: str = "http://localhost:8086"
    login_service_url: str = "http://localhost:8085"
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # "json" or "text"
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 100
    
    # Security
    csrf_enabled: bool = True
    csrf_secret_key: Optional[str] = None
    
    # External Services
    email_service_url: Optional[str] = None
    payment_gateway_url: Optional[str] = None
    
    # Feature Flags
    feature_search_enabled: bool = False
    feature_recommendations_enabled: bool = True
    feature_wishlist_enabled: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"  # Allow extra fields
    )


class DevelopmentSettings(Settings):
    """Development environment settings."""
    
    environment: str = "development"
    debug: bool = True
    reload: bool = True
    db_echo_sql: bool = True
    log_level: str = "DEBUG"
    
    # Relaxed CORS for development
    cors_origins: list[str] = ["*"]


class StagingSettings(Settings):
    """Staging environment settings."""
    
    environment: str = "staging"
    debug: bool = False
    reload: bool = False
    
    # Override with staging-specific values
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://yugabyte:yugabyte@staging-db:5433/yugabyte"
    )


class ProductionSettings(Settings):
    """Production environment settings."""
    
    environment: str = "production"
    debug: bool = False
    reload: bool = False
    db_echo_sql: bool = False
    log_level: str = "INFO"
    
    # Strict CORS for production
    cors_origins: list[str] = [
        "https://bookstore-r-us.com",
        "https://www.bookstore-r-us.com"
    ]
    
    # Require secure settings in production
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Validate production requirements
        if self.jwt_secret_key == "bookstore-secret-key-change-in-production":
            raise ValueError("JWT_SECRET_KEY must be set in production!")
        
        if self.csrf_enabled and not self.csrf_secret_key:
            raise ValueError("CSRF_SECRET_KEY must be set when CSRF is enabled!")


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (singleton).
    
    Settings are loaded once and cached for the application lifetime.
    Determined by ENVIRONMENT variable.
    
    Returns:
        Settings instance for current environment
    
    Usage:
        from shared.config import get_settings
        
        settings = get_settings()
        print(f"Running on {settings.environment}")
    """
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "staging":
        return StagingSettings()
    else:
        return DevelopmentSettings()


# Environment variable helper
def get_env(key: str, default: str = None) -> Optional[str]:
    """
    Get environment variable with optional default.
    
    Args:
        key: Environment variable name
        default: Default value if not set
    
    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)


# For testing
if __name__ == "__main__":
    print("Configuration Management Demo")
    print("=" * 50)
    
    # Load settings
    settings = get_settings()
    
    print(f"\nEnvironment: {settings.environment}")
    print(f"Debug Mode: {settings.debug}")
    print(f"Database: {settings.database_url[:50]}...")
    print(f"Redis: {settings.redis_url}")
    print(f"JWT Algorithm: {settings.jwt_algorithm}")
    print(f"CORS Origins: {settings.cors_origins}")
    print(f"Log Level: {settings.log_level}")
    
    print(f"\nFeature Flags:")
    print(f"  Search: {settings.feature_search_enabled}")
    print(f"  Recommendations: {settings.feature_recommendations_enabled}")
    print(f"  Wishlist: {settings.feature_wishlist_enabled}")
    
    print("\n✅ Configuration loaded successfully!")
