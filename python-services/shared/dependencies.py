"""
FastAPI dependency injection patterns for authentication.

Provides reusable dependencies for protecting routes with JWT authentication.
Integrates with the auth.py module for token verification.

Usage in FastAPI routes:
    from fastapi import Depends
    from shared.dependencies import get_current_user, require_admin
    
    @app.get("/protected")
    async def protected_route(user_id: str = Depends(get_current_user)):
        return {"user_id": user_id}
    
    @app.get("/admin-only")
    async def admin_route(user_id: str = Depends(require_admin)):
        return {"admin_user_id": user_id}
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth import verify_token, TokenData, TokenExpiredError, InvalidTokenError


# HTTP Bearer token security scheme
security = HTTPBearer(
    scheme_name="JWT Bearer Token",
    description="JWT token in format: Bearer <token>",
    auto_error=False  # Don't auto-raise, we'll handle errors
)


async def get_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """
    Extract JWT token from Authorization header.
    
    Expects header format: "Authorization: Bearer <token>"
    
    Args:
        credentials: HTTP authorization credentials from header
    
    Returns:
        JWT token string
    
    Raises:
        HTTPException: 401 if token is missing
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials


async def get_token_data(token: str = Depends(get_token)) -> TokenData:
    """
    Verify JWT token and extract payload data.
    
    Args:
        token: JWT token from get_token dependency
    
    Returns:
        TokenData object with user information
    
    Raises:
        HTTPException: 401 if token is expired or invalid
    """
    try:
        token_data = verify_token(token)
        return token_data
    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    token_data: TokenData = Depends(get_token_data)
) -> str:
    """
    Get the current authenticated user's ID.
    
    This is the primary dependency for protecting routes that require authentication.
    
    Args:
        token_data: Token data from get_token_data dependency
    
    Returns:
        User ID string
    
    Example:
        @app.get("/cart")
        async def get_cart(user_id: str = Depends(get_current_user)):
            # user_id is guaranteed to be authenticated
            return await cart_service.get_cart(user_id)
    """
    return token_data.user_id


async def get_current_user_email(
    token_data: TokenData = Depends(get_token_data)
) -> Optional[str]:
    """
    Get the current authenticated user's email.
    
    Args:
        token_data: Token data from get_token_data dependency
    
    Returns:
        Email address or None if not in token
    """
    return token_data.email


async def require_role(
    required_role: str,
    token_data: TokenData = Depends(get_token_data)
) -> str:
    """
    Require a specific role for access.
    
    Args:
        required_role: Role name required (e.g., "admin", "manager")
        token_data: Token data from get_token_data dependency
    
    Returns:
        User ID if role is present
    
    Raises:
        HTTPException: 403 if user doesn't have required role
    
    Note:
        For specific roles, use the convenience functions like require_admin()
    """
    if required_role not in token_data.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: requires '{required_role}' role",
        )
    
    return token_data.user_id


async def require_admin(
    token_data: TokenData = Depends(get_token_data)
) -> str:
    """
    Require admin role for access.
    
    Args:
        token_data: Token data from get_token_data dependency
    
    Returns:
        User ID if user is admin
    
    Raises:
        HTTPException: 403 if user is not an admin
    
    Example:
        @app.delete("/products/{asin}")
        async def delete_product(
            asin: str,
            admin_id: str = Depends(require_admin)
        ):
            # Only admins can reach this code
            await product_service.delete(asin)
    """
    if "admin" not in token_data.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: admin role required",
        )
    
    return token_data.user_id


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[str]:
    """
    Get current user ID if authenticated, None otherwise.
    
    Use for routes that work both for authenticated and anonymous users,
    but may behave differently (e.g., personalized recommendations).
    
    Args:
        credentials: HTTP authorization credentials (optional)
    
    Returns:
        User ID if authenticated, None otherwise
    
    Example:
        @app.get("/products")
        async def list_products(
            user_id: Optional[str] = Depends(get_optional_user)
        ):
            # Works for both authenticated and anonymous users
            products = await product_service.list_all()
            
            if user_id:
                # Add personalized recommendations
                products = await add_recommendations(products, user_id)
            
            return products
    """
    if credentials is None:
        return None
    
    try:
        token_data = verify_token(credentials.credentials)
        return token_data.user_id
    except (TokenExpiredError, InvalidTokenError):
        # Invalid token, treat as unauthenticated
        return None


# Role-based dependency factory
def require_any_role(*roles: str):
    """
    Create a dependency that requires any of the specified roles.
    
    Args:
        *roles: Variable number of role names
    
    Returns:
        Dependency function
    
    Example:
        from functools import partial
        
        require_staff = require_any_role("admin", "manager", "support")
        
        @app.get("/orders")
        async def list_orders(user_id: str = Depends(require_staff)):
            # Accessible to admin, manager, or support roles
            pass
    """
    async def dependency(token_data: TokenData = Depends(get_token_data)) -> str:
        if not any(role in token_data.roles for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: requires one of {roles}",
            )
        return token_data.user_id
    
    return dependency


# Convenience dependencies for common role combinations
require_staff = require_any_role("admin", "manager", "support")
require_manager = require_any_role("admin", "manager")


# For testing
if __name__ == "__main__":
    print("FastAPI Authentication Dependencies")
    print("=" * 50)
    print("\nAvailable dependencies:")
    print("  - get_current_user: Require authentication")
    print("  - get_optional_user: Optional authentication")
    print("  - require_admin: Require admin role")
    print("  - require_staff: Require admin, manager, or support role")
    print("  - require_manager: Require admin or manager role")
    print("\n✅ Dependencies module loaded successfully!")
