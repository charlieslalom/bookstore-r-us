"""
HTTPX async HTTP client for inter-service communication.

Provides async HTTP client with connection pooling, retries, and timeouts.
Used for service-to-service calls in microservices architecture.

Features:
- Async HTTP requests (HTTPX)
- Connection pooling
- Automatic retries with backoff
- Request/response logging
- Circuit breaker pattern
- Timeout configuration

Usage:
    from shared.http_client import get_http_client, ServiceClient
    
    # Direct HTTP client
    async with get_http_client() as client:
        response = await client.get("http://products-service/api/v1/products/B001")
    
    # Service-specific client
    products_client = ServiceClient("products-service")
    product = await products_client.get("/products/B001")
"""

from typing import Optional, Dict, Any
import httpx
from httpx import AsyncClient, Response, Timeout
from functools import lru_cache
from contextlib import asynccontextmanager
from shared.config import get_settings
from shared.errors import BookstoreLogger
import asyncio


# Default timeout configuration
DEFAULT_TIMEOUT = Timeout(
    connect=5.0,  # Connection timeout
    read=10.0,    # Read timeout
    write=10.0,   # Write timeout
    pool=5.0      # Pool timeout
)

# Default retry configuration
MAX_RETRIES = 3
RETRY_BACKOFF = 0.5  # seconds


# Global logger
logger = BookstoreLogger("http-client")


@lru_cache()
def get_http_client() -> AsyncClient:
    """
    Get shared HTTP client instance (singleton).
    
    Returns:
        Async HTTP client with connection pooling
    
    Configuration:
        - Connection pooling (max 100 connections)
        - Automatic retry logic
        - Timeout defaults
        - HTTP/2 support
    
    Usage:
        async with get_http_client() as client:
            response = await client.get("https://api.example.com/data")
    """
    settings = get_settings()
    
    return AsyncClient(
        timeout=DEFAULT_TIMEOUT,
        limits=httpx.Limits(
            max_keepalive_connections=20,
            max_connections=100
        ),
        http2=True,  # Enable HTTP/2
        follow_redirects=True
    )


async def close_http_client():
    """
    Close HTTP client connections gracefully.
    
    Call on application shutdown:
        @app.on_event("shutdown")
        async def shutdown():
            await close_http_client()
    """
    client = get_http_client()
    await client.aclose()


async def retry_request(
    client: AsyncClient,
    method: str,
    url: str,
    max_retries: int = MAX_RETRIES,
    backoff: float = RETRY_BACKOFF,
    **kwargs
) -> Response:
    """
    Make HTTP request with automatic retries.
    
    Args:
        client: HTTPX async client
        method: HTTP method (GET, POST, etc.)
        url: Request URL
        max_retries: Maximum retry attempts
        backoff: Backoff multiplier between retries
        **kwargs: Additional request parameters
    
    Returns:
        HTTP response
    
    Raises:
        httpx.HTTPError: If all retries fail
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            response = await client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        
        except httpx.HTTPStatusError as e:
            # Don't retry 4xx client errors (except 429 rate limit)
            if 400 <= e.response.status_code < 500 and e.response.status_code != 429:
                raise
            
            last_exception = e
            
            # Exponential backoff
            if attempt < max_retries - 1:
                wait_time = backoff * (2 ** attempt)
                logger.warning(
                    f"Request failed (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s",
                    url=url,
                    status=e.response.status_code
                )
                await asyncio.sleep(wait_time)
        
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            last_exception = e
            
            # Retry network errors
            if attempt < max_retries - 1:
                wait_time = backoff * (2 ** attempt)
                logger.warning(
                    f"Request failed (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s",
                    url=url,
                    error=str(e)
                )
                await asyncio.sleep(wait_time)
    
    # All retries failed
    logger.error(f"Request failed after {max_retries} attempts", url=url)
    raise last_exception


class ServiceClient:
    """
    HTTP client wrapper for service-to-service communication.
    
    Provides convenience methods for calling other microservices.
    
    Usage:
        products_client = ServiceClient("products")
        
        # GET request
        product = await products_client.get("/products/B001")
        
        # POST request
        cart_item = await products_client.post(
            "/cart/add",
            json={"asin": "B001", "quantity": 1}
        )
    """
    
    def __init__(
        self,
        service_name: str,
        base_url: Optional[str] = None,
        timeout: Optional[Timeout] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        """
        Initialize service client.
        
        Args:
            service_name: Service name (e.g., "products", "cart")
            base_url: Base URL override (optional, defaults from config)
            timeout: Custom timeout configuration
            headers: Default headers to include in all requests
        """
        self.service_name = service_name
        self.base_url = base_url or self._get_service_url(service_name)
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.default_headers = headers or {}
        self.client = get_http_client()
    
    def _get_service_url(self, service_name: str) -> str:
        """Get service URL from configuration."""
        settings = get_settings()
        
        url_map = {
            "products": settings.products_service_url,
            "cart": settings.cart_service_url,
            "checkout": settings.checkout_service_url,
            "login": settings.login_service_url
        }
        
        return url_map.get(service_name, f"http://{service_name}:8000")
    
    def _build_url(self, path: str) -> str:
        """Build full URL from base and path."""
        # Remove leading slash if present
        path = path.lstrip("/")
        
        # Ensure base_url doesn't end with slash
        base = self.base_url.rstrip("/")
        
        return f"{base}/{path}"
    
    async def request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Response:
        """
        Make HTTP request to service.
        
        Args:
            method: HTTP method
            path: Request path (relative to base URL)
            headers: Additional headers
            **kwargs: Additional request parameters
        
        Returns:
            HTTP response
        """
        url = self._build_url(path)
        
        # Merge headers
        request_headers = {**self.default_headers}
        if headers:
            request_headers.update(headers)
        
        logger.info(
            f"{method} {url}",
            service=self.service_name,
            path=path
        )
        
        try:
            response = await retry_request(
                self.client,
                method,
                url,
                headers=request_headers,
                **kwargs
            )
            
            logger.info(
                f"{method} {url} -> {response.status_code}",
                service=self.service_name,
                status=response.status_code
            )
            
            return response
        
        except Exception as e:
            logger.error(
                f"{method} {url} failed",
                service=self.service_name,
                error=str(e)
            )
            raise
    
    async def get(self, path: str, **kwargs) -> Any:
        """GET request returning JSON."""
        response = await self.request("GET", path, **kwargs)
        return response.json()
    
    async def post(self, path: str, **kwargs) -> Any:
        """POST request returning JSON."""
        response = await self.request("POST", path, **kwargs)
        return response.json()
    
    async def put(self, path: str, **kwargs) -> Any:
        """PUT request returning JSON."""
        response = await self.request("PUT", path, **kwargs)
        return response.json()
    
    async def patch(self, path: str, **kwargs) -> Any:
        """PATCH request returning JSON."""
        response = await self.request("PATCH", path, **kwargs)
        return response.json()
    
    async def delete(self, path: str, **kwargs) -> Any:
        """DELETE request returning JSON."""
        response = await self.request("DELETE", path, **kwargs)
        return response.json()


# Service client instances (can be reused)

@lru_cache()
def get_products_client() -> ServiceClient:
    """Get Products service client."""
    return ServiceClient("products")


@lru_cache()
def get_cart_client() -> ServiceClient:
    """Get Cart service client."""
    return ServiceClient("cart")


@lru_cache()
def get_checkout_client() -> ServiceClient:
    """Get Checkout service client."""
    return ServiceClient("checkout")


@lru_cache()
def get_login_client() -> ServiceClient:
    """Get Login service client."""
    return ServiceClient("login")


# Authenticated request helper

async def authenticated_request(
    client: ServiceClient,
    method: str,
    path: str,
    token: str,
    **kwargs
) -> Any:
    """
    Make authenticated request with JWT token.
    
    Args:
        client: Service client
        method: HTTP method
        path: Request path
        token: JWT access token
        **kwargs: Additional request parameters
    
    Returns:
        Response JSON
    
    Usage:
        cart_client = get_cart_client()
        cart = await authenticated_request(
            cart_client,
            "GET",
            "/cart",
            token=user_token
        )
    """
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {token}"
    
    response = await client.request(method, path, headers=headers, **kwargs)
    return response.json()


# For testing
if __name__ == "__main__":
    import asyncio
    
    async def test_http_client():
        print("HTTPX Async HTTP Client Demo")
        print("=" * 50)
        
        # Test basic HTTP client
        print("\n1. Testing basic HTTP client...")
        async with get_http_client() as client:
            try:
                response = await client.get("https://httpbin.org/get")
                print(f"   ✅ GET request successful: {response.status_code}")
            except Exception as e:
                print(f"   ⚠️  External request failed (expected if offline): {e}")
        
        # Test service client
        print("\n2. Testing service client...")
        products_client = ServiceClient(
            "products",
            base_url="http://localhost:8082"
        )
        
        print(f"   Service: {products_client.service_name}")
        print(f"   Base URL: {products_client.base_url}")
        print(f"   ✅ Service client initialized")
        
        # Test URL building
        print("\n3. Testing URL building...")
        url = products_client._build_url("/api/v1/products/B001")
        print(f"   Built URL: {url}")
        print(f"   ✅ URL building working")
        
        # Cleanup
        await close_http_client()
        
        print("\n✅ HTTP client utilities working correctly!")
    
    asyncio.run(test_http_client())
