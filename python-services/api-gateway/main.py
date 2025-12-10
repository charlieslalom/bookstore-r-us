"""
API Gateway Microservice - FastAPI
Routes external requests to backend microservices
"""
import os
import sys
from pathlib import Path

# Add parent directory to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import uvicorn
from typing import Optional

app = FastAPI(
    title="API Gateway",
    description="Central routing for all microservices",
    version="1.0.0"
)

# Service URLs from environment variables
PRODUCTS_SERVICE_URL = os.getenv("PRODUCTS_SERVICE_URL", "http://localhost:8082")
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://localhost:8083")
CHECKOUT_SERVICE_URL = os.getenv("CHECKOUT_SERVICE_URL", "http://localhost:8084")
LOGIN_SERVICE_URL = os.getenv("LOGIN_SERVICE_URL", "http://localhost:8085")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:1123",
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# HTTP client for proxying requests
client = httpx.AsyncClient(timeout=30.0)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "api-gateway",
        "status": "running",
        "version": "1.0.0",
        "services": {
            "products": PRODUCTS_SERVICE_URL,
            "cart": CART_SERVICE_URL,
            "checkout": CHECKOUT_SERVICE_URL,
            "login": LOGIN_SERVICE_URL
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api-gateway"}


async def proxy_request(
    service_url: str,
    path: str,
    request: Request
):
    """Proxy a request to a backend service"""
    # Build target URL
    target_url = f"{service_url}{path}"
    
    # Forward query parameters
    if request.url.query:
        target_url = f"{target_url}?{request.url.query}"
    
    # Forward headers (excluding host)
    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in ["host", "content-length"]
    }
    
    try:
        # Forward the request to the backend service
        if request.method == "GET":
            response = await client.get(target_url, headers=headers)
        elif request.method == "POST":
            body = await request.body()
            response = await client.post(target_url, headers=headers, content=body)
        elif request.method == "PUT":
            body = await request.body()
            response = await client.put(target_url, headers=headers, content=body)
        elif request.method == "DELETE":
            response = await client.delete(target_url, headers=headers)
        else:
            return JSONResponse(
                status_code=405,
                content={"error": "Method not allowed"}
            )
        
        # Return the response from the backend service
        return JSONResponse(
            status_code=response.status_code,
            content=response.json() if response.headers.get("content-type", "").startswith("application/json") else {"data": response.text},
            headers=dict(response.headers)
        )
    
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"Service unavailable: {service_url}"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail=f"Service timeout: {service_url}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gateway error: {str(e)}"
        )


@app.api_route("/products-microservice/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def products_proxy(path: str, request: Request):
    """Proxy requests to products microservice"""
    return await proxy_request(PRODUCTS_SERVICE_URL, f"/products-microservice/{path}", request)


@app.api_route("/cart-microservice/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def cart_proxy(path: str, request: Request):
    """Proxy requests to cart microservice"""
    return await proxy_request(CART_SERVICE_URL, f"/cart-microservice/{path}", request)


@app.api_route("/checkout-microservice/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def checkout_proxy(path: str, request: Request):
    """Proxy requests to checkout microservice"""
    return await proxy_request(CHECKOUT_SERVICE_URL, f"/checkout-microservice/{path}", request)


@app.api_route("/login-microservice/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def login_proxy(path: str, request: Request):
    """Proxy requests to login microservice"""
    return await proxy_request(LOGIN_SERVICE_URL, f"/login-microservice/{path}", request)


@app.on_event("shutdown")
async def shutdown_event():
    """Close HTTP client on shutdown"""
    await client.aclose()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8081"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

