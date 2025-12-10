"""
Products Microservice - FastAPI
Provides product catalog endpoints compatible with existing Java service
"""
import os
import sys
from pathlib import Path

# Add parent directory to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn

# Import shared utilities
try:
    from shared.config import get_settings
    from shared.errors import setup_error_handlers
    from shared.database import get_engine, get_session
    settings = get_settings()
except ImportError:
    # Fallback if shared modules not available
    class MockSettings:
        app_name = "products-service"
        cors_origins = ["http://localhost:3000", "http://localhost:3001", "http://localhost:1123"]
    settings = MockSettings()

app = FastAPI(
    title="Products Microservice",
    description="Product catalog management",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins if hasattr(settings, 'cors_origins') else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup error handlers if available
try:
    setup_error_handlers(app)
except:
    pass


# Mock product data for testing (until database is connected)
MOCK_PRODUCTS = {
    "Books": [
        {"asin": "B001", "title": "The Great Gatsby", "category": "Books", "price": 12.99, "imUrl": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=600&fit=crop", "author": "F. Scott Fitzgerald"},
        {"asin": "B002", "title": "To Kill a Mockingbird", "category": "Books", "price": 14.99, "imUrl": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400&h=600&fit=crop", "author": "Harper Lee"},
        {"asin": "B003", "title": "1984", "category": "Books", "price": 13.99, "imUrl": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=600&fit=crop", "author": "George Orwell"},
        {"asin": "B004", "title": "Pride and Prejudice", "category": "Books", "price": 11.99, "imUrl": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400&h=600&fit=crop", "author": "Jane Austen"},
    ],
    "Electronics": [
        {"asin": "E001", "title": "Wireless Headphones", "category": "Electronics", "price": 79.99, "imUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=600&fit=crop"},
        {"asin": "E002", "title": "Bluetooth Speaker", "category": "Electronics", "price": 49.99, "imUrl": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=600&fit=crop"},
        {"asin": "E003", "title": "USB-C Cable", "category": "Electronics", "price": 12.99, "imUrl": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400&h=600&fit=crop"},
        {"asin": "E004", "title": "Laptop Stand", "category": "Electronics", "price": 34.99, "imUrl": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=600&fit=crop"},
    ],
    "Music": [
        {"asin": "M001", "title": "Classic Vinyl Collection", "category": "Music", "price": 89.99, "imUrl": "https://images.unsplash.com/photo-1619983081563-430f63602796?w=400&h=600&fit=crop"},
        {"asin": "M002", "title": "Guitar Strings Set", "category": "Music", "price": 15.99, "imUrl": "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=400&h=600&fit=crop"},
        {"asin": "M003", "title": "Piano Sheet Music", "category": "Music", "price": 19.99, "imUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=600&fit=crop"},
        {"asin": "M004", "title": "Drum Sticks", "category": "Music", "price": 22.99, "imUrl": "https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=400&h=600&fit=crop"},
    ],
    "Beauty": [
        {"asin": "BT001", "title": "Moisturizing Cream", "category": "Beauty", "price": 24.99, "imUrl": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=600&fit=crop"},
        {"asin": "BT002", "title": "Facial Cleanser", "category": "Beauty", "price": 18.99, "imUrl": "https://images.unsplash.com/photo-1571875257727-256c39da42af?w=400&h=600&fit=crop"},
        {"asin": "BT003", "title": "Hair Serum", "category": "Beauty", "price": 29.99, "imUrl": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400&h=600&fit=crop"},
        {"asin": "BT004", "title": "Makeup Brush Set", "category": "Beauty", "price": 39.99, "imUrl": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=600&fit=crop"},
    ],
}


@app.get("/")
async def root():
    """Root endpoint"""
    return {"service": "products-microservice", "status": "running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "products-microservice"}


@app.get("/products-microservice/products/category/{category}")
async def get_products_by_category(
    category: str,
    page: int = Query(0, ge=0),
    size: int = Query(20, ge=1, le=100)
):
    """
    Get products by category with pagination
    Compatible with Java service API
    """
    # Get products for category
    products = MOCK_PRODUCTS.get(category, [])
    
    # Calculate pagination
    total = len(products)
    start = page * size
    end = start + size
    
    # Return paginated response in same format as Java service
    return {
        "content": products[start:end],
        "totalElements": total,
        "totalPages": (total + size - 1) // size,
        "size": size,
        "number": page,
        "numberOfElements": len(products[start:end]),
        "first": page == 0,
        "last": end >= total,
        "empty": total == 0
    }


@app.get("/products-microservice/products/{asin}")
async def get_product_by_asin(asin: str):
    """Get a single product by ASIN"""
    # Search all categories for the product
    for category, products in MOCK_PRODUCTS.items():
        for product in products:
            if product["asin"] == asin:
                return product
    
    raise HTTPException(status_code=404, detail=f"Product not found: {asin}")


@app.get("/products-microservice/categories")
async def get_categories():
    """Get all product categories"""
    return {
        "categories": list(MOCK_PRODUCTS.keys())
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8082"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

