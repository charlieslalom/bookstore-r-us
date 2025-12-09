from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from typing import List, Any, Generic, TypeVar
from pydantic import BaseModel
from database import get_session
from models import ProductMetadata, ProductRanking

router = APIRouter(prefix="/products-microservice", tags=["products"])

# Paginated response model to match Spring Boot Page format
class PageResponse(BaseModel):
    content: List[Any]
    totalElements: int
    totalPages: int
    size: int
    number: int  # page number (0-indexed)

@router.get("/product/{asin}", response_model=ProductMetadata)
def get_product_details(asin: str, session: Session = Depends(get_session)):
    product = session.get(ProductMetadata, asin)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/products")
def get_products(
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    offset = page * size
    statement = select(ProductMetadata).offset(offset).limit(size)
    products = session.exec(statement).all()

    # Get total count
    count_statement = select(func.count()).select_from(ProductMetadata)
    total = session.exec(count_statement).one()

    return PageResponse(
        content=[p.model_dump() for p in products],
        totalElements=total,
        totalPages=(total + size - 1) // size,
        size=size,
        number=page
    )

@router.get("/products/category/{category}")
def get_products_by_category(
    category: str,
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    offset = page * size
    statement = select(ProductRanking).where(ProductRanking.category == category).offset(offset).limit(size)
    rankings = session.exec(statement).all()

    # Get total count for this category
    count_statement = select(func.count()).select_from(ProductRanking).where(ProductRanking.category == category)
    total = session.exec(count_statement).one()

    return PageResponse(
        content=[r.model_dump() for r in rankings],
        totalElements=total,
        totalPages=(total + size - 1) // size,
        size=size,
        number=page
    )
