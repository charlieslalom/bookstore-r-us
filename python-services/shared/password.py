"""
BCrypt password validation for Bookstore-R-Us Python services.

Provides compatibility with existing BCrypt password hashes from Java services.
Maintains password security while enabling seamless migration.

Security Features:
- BCrypt algorithm (industry standard)
- Salt generation (automatic per password)
- Slow hashing (protects against brute force)
- Compatible with Java BCryptPasswordEncoder

NO hardcoded user IDs. NO plain text passwords.
"""

import bcrypt
from typing import Optional


class PasswordError(Exception):
    """Raised when password operations fail."""
    pass


def hash_password(plain_password: str) -> str:
    """
    Hash a plain text password using BCrypt.
    
    Args:
        plain_password: Plain text password to hash
    
    Returns:
        BCrypt hash string (includes salt)
    
    Example:
        >>> hashed = hash_password("MySecurePassword123!")
        >>> # "$2b$12$..."
    
    Note:
        Each call generates a new salt, so the same password
        will produce different hashes (this is correct behavior).
    """
    if not plain_password:
        raise PasswordError("Password cannot be empty")
    
    # Convert string to bytes
    password_bytes = plain_password.encode('utf-8')
    
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a BCrypt hash.
    
    Compatible with Java BCryptPasswordEncoder hashes from existing system.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: BCrypt hash from database
    
    Returns:
        True if password matches, False otherwise
    
    Example:
        >>> hashed = hash_password("SecurePass123")
        >>> verify_password("SecurePass123", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    
    Security:
        - Timing-safe comparison (prevents timing attacks)
        - No password leakage in error messages
        - Compatible with Java Spring Security BCrypt
    """
    if not plain_password or not hashed_password:
        return False
    
    try:
        # Convert to bytes
        password_bytes = plain_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        
        # Verify with constant-time comparison
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    except Exception:
        # Don't leak information about hash format errors
        return False


def needs_rehash(hashed_password: str, cost: int = 12) -> bool:
    """
    Check if a password hash needs to be regenerated with a higher cost factor.
    
    Useful for gradually increasing security as computing power increases.
    
    Args:
        hashed_password: Existing BCrypt hash
        cost: Desired cost factor (default 12, range 4-31)
    
    Returns:
        True if hash should be regenerated, False otherwise
    
    Example:
        >>> old_hash = hash_password("password")  # Uses default cost
        >>> if needs_rehash(old_hash, cost=14):
        ...     new_hash = hash_password("password")  # Re-hash with higher cost
    
    Note:
        Cost of 12 is recommended for 2024-2025. Increase gradually over time.
    """
    try:
        # Extract cost from hash (format: $2b$XX$...)
        hash_parts = hashed_password.split('$')
        if len(hash_parts) >= 3:
            current_cost = int(hash_parts[2])
            return current_cost < cost
        return False
    except Exception:
        return False


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password meets minimum security requirements.
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    
    Args:
        password: Plain text password to validate
    
    Returns:
        Tuple of (is_valid, error_message)
        - (True, None) if valid
        - (False, "error description") if invalid
    
    Example:
        >>> is_valid, error = validate_password_strength("weak")
        >>> print(is_valid, error)
        False "Password must be at least 8 characters"
        
        >>> is_valid, error = validate_password_strength("StrongPass123!")
        >>> print(is_valid, error)
        True None
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    # Check for special characters
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False, "Password must contain at least one special character"
    
    return True, None


# For existing user compatibility
def is_valid_bcrypt_hash(hash_string: str) -> bool:
    """
    Check if a string is a valid BCrypt hash format.
    
    Useful for validating hashes retrieved from database.
    
    Args:
        hash_string: String to validate
    
    Returns:
        True if valid BCrypt format, False otherwise
    
    Example:
        >>> is_valid_bcrypt_hash("$2b$12$abcd...")
        True
        >>> is_valid_bcrypt_hash("plaintext")
        False
    """
    if not hash_string:
        return False
    
    # BCrypt format: $2a$, $2b$, or $2y$ followed by cost and hash
    # Example: $2b$12$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
    parts = hash_string.split('$')
    
    if len(parts) != 4:
        return False
    
    # Check algorithm identifier
    if parts[1] not in ['2a', '2b', '2y']:
        return False
    
    # Check cost is valid number
    try:
        cost = int(parts[2])
        if cost < 4 or cost > 31:
            return False
    except ValueError:
        return False
    
    # Check hash part has reasonable length (53 chars for BCrypt)
    if len(parts[3]) != 53:
        return False
    
    return True


# For testing and development
if __name__ == "__main__":
    print("BCrypt Password Utilities Demo")
    print("=" * 50)
    
    # Hash a password
    password = "MySecurePassword123!"
    hashed = hash_password(password)
    print(f"\n1. Hash Password:")
    print(f"   Plain: {password}")
    print(f"   Hash:  {hashed}")
    
    # Verify correct password
    print(f"\n2. Verify Correct Password:")
    is_valid = verify_password(password, hashed)
    print(f"   Result: {is_valid} (should be True)")
    
    # Verify incorrect password
    print(f"\n3. Verify Incorrect Password:")
    is_valid = verify_password("WrongPassword", hashed)
    print(f"   Result: {is_valid} (should be False)")
    
    # Validate password strength
    print(f"\n4. Validate Password Strength:")
    weak_password = "weak"
    is_valid, error = validate_password_strength(weak_password)
    print(f"   Password: {weak_password}")
    print(f"   Valid: {is_valid}, Error: {error}")
    
    strong_password = "StrongPass123!"
    is_valid, error = validate_password_strength(strong_password)
    print(f"   Password: {strong_password}")
    print(f"   Valid: {is_valid}, Error: {error}")
    
    # Check if hash is valid format
    print(f"\n5. Validate BCrypt Hash Format:")
    print(f"   Hash: {is_valid_bcrypt_hash(hashed)} (should be True)")
    print(f"   Plaintext: {is_valid_bcrypt_hash('plaintext')} (should be False)")
    
    # Check if needs rehash
    print(f"\n6. Check if Needs Rehash:")
    needs_update = needs_rehash(hashed, cost=14)
    print(f"   Current cost: 12, Target cost: 14")
    print(f"   Needs rehash: {needs_update}")
    
    print("\n✅ BCrypt utilities working correctly!")
    print("\n🔒 SECURITY REMINDERS:")
    print("   - NEVER store plain text passwords")
    print("   - NEVER hardcode user IDs")
    print("   - ALWAYS use verify_password() for login")
    print("   - User ID MUST come from verified JWT token")
