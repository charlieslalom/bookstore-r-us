"""
Error handling and logging infrastructure for Bookstore-R-Us Python services.

Provides standardized error handling, custom exceptions, and structured logging.

Features:
- Custom exception classes for different error types
- HTTP exception handlers for FastAPI
- Structured logging with context
- Request ID tracking
- Error response formatting

Usage in FastAPI:
    from fastapi import FastAPI
    from shared.errors import setup_error_handlers, BookstoreException
    
    app = FastAPI()
    setup_error_handlers(app)
"""

from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import sys
import traceback
from datetime import datetime
import uuid


# Configure logging format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


# Base exception class
class BookstoreException(Exception):
    """
    Base exception for all Bookstore-R-Us errors.
    
    Attributes:
        message: Human-readable error message
        code: Application-specific error code
        status_code: HTTP status code
        details: Additional error context
    """
    
    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


# Specific exception types
class NotFoundException(BookstoreException):
    """Resource not found."""
    
    def __init__(self, resource: str, identifier: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"{resource} not found: {identifier}",
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details or {"resource": resource, "identifier": identifier}
        )


class ValidationException(BookstoreException):
    """Input validation failed."""
    
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details or {"field": field} if field else details
        )


class UnauthorizedException(BookstoreException):
    """Authentication required or failed."""
    
    def __init__(self, message: str = "Authentication required", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )


class ForbiddenException(BookstoreException):
    """Insufficient permissions."""
    
    def __init__(self, message: str = "Access denied", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=status.HTTP_403_FORBIDDEN,
            details=details
        )


class ConflictException(BookstoreException):
    """Resource conflict (e.g., duplicate key)."""
    
    def __init__(self, message: str, resource: Optional[str] = None, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=status.HTTP_409_CONFLICT,
            details=details or {"resource": resource} if resource else details
        )


class ServiceUnavailableException(BookstoreException):
    """Service temporarily unavailable."""
    
    def __init__(self, message: str = "Service temporarily unavailable", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            code="SERVICE_UNAVAILABLE",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )


# Error response formatter
def format_error_response(
    request_id: str,
    code: str,
    message: str,
    status_code: int,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format error response in standard structure.
    
    Returns:
        Dictionary with error information
    """
    return {
        "error": {
            "code": code,
            "message": message,
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details or {}
        },
        "status": status_code
    }


# Exception handlers
async def bookstore_exception_handler(request: Request, exc: BookstoreException):
    """Handle BookstoreException and subclasses."""
    request_id = getattr(request.state, "request_id", "unknown")
    
    # Log error
    logger = logging.getLogger("bookstore")
    logger.error(
        f"{exc.code}: {exc.message}",
        extra={
            "request_id": request_id,
            "path": request.url.path,
            "details": exc.details
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            request_id=request_id,
            code=exc.code,
            message=exc.message,
            status_code=exc.status_code,
            details=exc.details
        )
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle FastAPI validation errors."""
    request_id = getattr(request.state, "request_id", "unknown")
    
    # Extract validation errors
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=format_error_response(
            request_id=request_id,
            code="VALIDATION_ERROR",
            message="Input validation failed",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"errors": errors}
        )
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle Starlette HTTP exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            request_id=request_id,
            code="HTTP_ERROR",
            message=exc.detail,
            status_code=exc.status_code
        )
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    
    # Log full traceback
    logger = logging.getLogger("bookstore")
    logger.error(
        f"Unexpected error: {str(exc)}",
        extra={"request_id": request_id, "path": request.url.path},
        exc_info=True
    )
    
    # Don't expose internal error details in production
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error_response(
            request_id=request_id,
            code="INTERNAL_ERROR",
            message="An unexpected error occurred",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"error": str(exc)}  # Remove in production
        )
    )


# Middleware for request ID tracking
async def add_request_id_middleware(request: Request, call_next):
    """
    Add request ID to all requests for tracing.
    
    Request ID is:
    1. Extracted from X-Request-ID header if present
    2. Generated as UUID if not present
    3. Added to request.state for logging
    4. Added to response headers
    """
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Process request
    response = await call_next(request)
    
    # Add request ID to response
    response.headers["X-Request-ID"] = request_id
    
    return response


# Setup function
def setup_error_handlers(app: FastAPI):
    """
    Register all error handlers and middleware.
    
    Call this during FastAPI app initialization:
        from fastapi import FastAPI
        from shared.errors import setup_error_handlers
        
        app = FastAPI()
        setup_error_handlers(app)
    
    Args:
        app: FastAPI application instance
    """
    # Register exception handlers
    app.add_exception_handler(BookstoreException, bookstore_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    # Add request ID middleware
    app.middleware("http")(add_request_id_middleware)


# Structured logger
class BookstoreLogger:
    """
    Structured logger with request context.
    
    Usage:
        logger = BookstoreLogger("products-service")
        logger.info("Product retrieved", product_id="B001", user_id="u1001")
    """
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def _log(self, level: int, message: str, **context):
        """Log with structured context."""
        extra = {"request_id": context.pop("request_id", "no-request")}
        extra.update(context)
        self.logger.log(level, message, extra=extra)
    
    def debug(self, message: str, **context):
        self._log(logging.DEBUG, message, **context)
    
    def info(self, message: str, **context):
        self._log(logging.INFO, message, **context)
    
    def warning(self, message: str, **context):
        self._log(logging.WARNING, message, **context)
    
    def error(self, message: str, **context):
        self._log(logging.ERROR, message, **context)
    
    def critical(self, message: str, **context):
        self._log(logging.CRITICAL, message, **context)


# For testing
if __name__ == "__main__":
    print("Error Handling & Logging Demo")
    print("=" * 50)
    
    # Test logger
    logger = BookstoreLogger("test-service")
    logger.info("Service started", version="1.0.0")
    logger.warning("Low inventory", product="B001", quantity=5)
    
    # Test exceptions
    try:
        raise NotFoundException("Product", "B999")
    except BookstoreException as e:
        print(f"\n✅ Exception caught: {e.code} - {e.message}")
    
    print("\n✅ Error handling utilities working correctly!")
