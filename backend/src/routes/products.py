from fastapi import (
    APIRouter,
    Depends,
    Query,
    UploadFile,
    Request,
    File,
    Form,
    Request,
    status,
)
from src.config import get_settings, Settings
from src.models import Product
from src.controllers.ProductController import ProductController
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from src.config import get_settings
import os
from bson import ObjectId
from typing import Optional
from src.controllers.ProductController import db_client

app_settings = get_settings()
product_router = APIRouter(prefix="/products", tags=["products"])

db_client = AsyncIOMotorClient(app_settings.MONGODB_URI)


def get_product_controller(request: Request) -> ProductController:
    """Dependency to get ProductController instance"""
    return ProductController(request.app.state.db_client)


product_router = APIRouter(prefix="/api/v1/products", tags=["products"])


def get_product_controller():
    return ProductController(db_client)


@product_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(
    request: Request,
    title: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    images: List[UploadFile] = File(...),
    description: Optional[str] = Form(None),
    discount: Optional[float] = Form(0.0),
    stock: int = Form(...),
    controller: ProductController = Depends(get_product_controller),
):
    return await controller.create_product(
        request=request,
        title=title,
        price=price,
        images=images,
        category=category,
        description=description,
        stock=stock,
        discount=discount,
    )


@product_router.get("/{product_id}", response_model=dict)
async def get_product(
    product_id: str, controller: ProductController = Depends(get_product_controller)
):
    """Get a product by ID"""
    return await controller.get_product(product_id)


@product_router.get("/", response_model=List[dict])
async def get_all_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    controller: ProductController = Depends(get_product_controller),
):
    """Get all products with pagination"""
    return await controller.get_all_products(skip, limit)


@product_router.put("/{product_id}")
async def update_product_endpoint(
    request: Request,
    product_id: str,
    title: Optional[str] = Form(None),
    category: str = Form(...),
    price: Optional[float] = Form(None),
    description: Optional[str] = Form(None),
    discount: Optional[float] = Form(None),
    stock: Optional[int] = Form(None),
    images: Optional[List[UploadFile]] = File(...),
    controller: ProductController = Depends(get_product_controller),
):
    return await controller.update_product(
        request,
        product_id=product_id,
        category=category,
        title=title,
        price=price,
        description=description,
        discount=discount,
        stock=stock,
        images=images,
    )


@product_router.delete("/{product_id}", response_model=dict)
async def delete_product(
    product_id: str, controller: ProductController = Depends(get_product_controller)
):
    """Delete a product by ID"""
    return await controller.delete_product(product_id)


@product_router.get("/search/query", response_model=List[dict])
async def search_products(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    controller: ProductController = Depends(get_product_controller),
):
    """Search products by title or description"""
    return await controller.search_products(q, skip, limit)


@product_router.get("/filter/price", response_model=List[dict])
async def filter_by_price(
    min_price: int = Query(0, ge=0),
    max_price: int = Query(999999, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    controller: ProductController = Depends(get_product_controller),
):
    """Filter products by price range"""
    return await controller.filter_by_price(min_price, max_price, skip, limit)
