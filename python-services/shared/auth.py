"""
JWT Authentication utilities for Bookstore-R-Us Python services.

Provides token generation, validation, and user extraction for stateless authentication.
Compatible with existing BCrypt password hashes from Java services.

Security Features:
- Access tokens (15 minutes lifetime)
- Refresh tokens (7 days lifetime)
- HS256 algorithm (symmetric key)
- Token expiration validation
- Signature verification
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from jwt.exceptions import JWTError, ExpiredSignatureError, InvalidTokenError
import os
from dataclasses import dataclass


# Configuration - Override via environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "bookstore-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


@dataclass
class TokenData:
    """Decoded token payload."""
    user_id: str
    email: Optional[str] = None
    roles: list[str] = None
    token_type: str = "access"
    
    def __post_init__(self):
        if self.roles is None:
            self.roles = ["user"]


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


class TokenExpiredError(AuthenticationError):
    """Raised when token has expired."""
    pass


class InvalidTokenError(AuthenticationError):
    """Raised when token is invalid."""
    pass


def create_access_token(
    user_id: str,
    email: Optional[str] = None,
    roles: Optional[list[str]] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        user_id: Unique user identifier
        email: User's email address (optional)
        roles: List of user roles (optional, defaults to ["user"])
        expires_delta: Custom expiration time (optional)
    
    Returns:
        Encoded JWT token string
    
    Example:
        >>> token = create_access_token(user_id="u1001", email="user@example.com")
        >>> # Token valid for 15 minutes
    """
    if roles is None:
        roles = ["user"]
    
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.utcnow() + expires_delta
    
    payload = {
        "sub": user_id,  # Subject (user ID)
        "email": email,
        "roles": roles,
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at
        "type": "access"
    }
    
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    user_id: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        user_id: Unique user identifier
        expires_delta: Custom expiration time (optional, defaults to 7 days)
    
    Returns:
        Encoded JWT refresh token string
    
    Example:
        >>> refresh_token = create_refresh_token(user_id="u1001")
        >>> # Token valid for 7 days
    """
    if expires_delta is None:
        expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    expire = datetime.utcnow() + expires_delta
    
    payload = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    }
    
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        TokenData object with decoded payload
    
    Raises:
        TokenExpiredError: If token has expired
        InvalidTokenError: If token is invalid or signature doesn't match
    
    Example:
        >>> token_data = verify_token(token)
        >>> print(token_data.user_id)  # "u1001"
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise InvalidTokenError("Token missing 'sub' claim (user_id)")
        
        email: Optional[str] = payload.get("email")
        roles: list[str] = payload.get("roles", ["user"])
        token_type: str = payload.get("type", "access")
        
        return TokenData(
            user_id=user_id,
            email=email,
            roles=roles,
            token_type=token_type
        )
    
    except ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
    except JWTError as e:
        raise InvalidTokenError(f"Invalid token: {str(e)}")


def extract_user_id(token: str) -> str:
    """
    Extract user ID from token without full validation.
    
    Useful for quick user ID extraction when validation happens elsewhere.
    
    Args:
        token: JWT token string
    
    Returns:
        User ID string
    
    Raises:
        InvalidTokenError: If token cannot be decoded
    
    Example:
        >>> user_id = extract_user_id(token)
        >>> # "u1001"
    """
    try:
        # Decode without verification (for quick extraction)
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload.get("sub")
        
        if user_id is None:
            raise InvalidTokenError("Token missing 'sub' claim")
        
        return user_id
    except JWTError as e:
        raise InvalidTokenError(f"Cannot decode token: {str(e)}")


def create_token_pair(
    user_id: str,
    email: Optional[str] = None,
    roles: Optional[list[str]] = None
) -> Dict[str, str]:
    """
    Create both access and refresh tokens.
    
    Args:
        user_id: Unique user identifier
        email: User's email address (optional)
        roles: List of user roles (optional)
    
    Returns:
        Dictionary with 'access_token' and 'refresh_token' keys
    
    Example:
        >>> tokens = create_token_pair(user_id="u1001", email="user@example.com")
        >>> access_token = tokens["access_token"]
        >>> refresh_token = tokens["refresh_token"]
    """
    return {
        "access_token": create_access_token(user_id, email, roles),
        "refresh_token": create_refresh_token(user_id),
        "token_type": "bearer"
    }


# For testing and development
if __name__ == "__main__":
    # Example usage
    print("JWT Authentication Utilities Demo")
    print("=" * 50)
    
    # Create tokens
    tokens = create_token_pair(
        user_id="u1001",
        email="test@bookstore.com",
        roles=["user", "customer"]
    )
    
    print("\n1. Generated Tokens:")
    print(f"Access Token: {tokens['access_token'][:50]}...")
    print(f"Refresh Token: {tokens['refresh_token'][:50]}...")
    
    # Verify access token
    print("\n2. Verifying Access Token:")
    token_data = verify_token(tokens["access_token"])
    print(f"User ID: {token_data.user_id}")
    print(f"Email: {token_data.email}")
    print(f"Roles: {token_data.roles}")
    print(f"Token Type: {token_data.token_type}")
    
    # Extract user ID quickly
    print("\n3. Quick User ID Extraction:")
    user_id = extract_user_id(tokens["access_token"])
    print(f"User ID: {user_id}")
    
    print("\n✅ JWT utilities working correctly!")
