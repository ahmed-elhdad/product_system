import os
from fastapi import UploadFile, HTTPException, Request
from bson import ObjectId
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import ReturnDocument
from src.config import get_settings
from src.models import Product
from src.config import get_settings
from .BaseController import BaseController

app_settings = get_settings()
db_client = AsyncIOMotorClient(app_settings.MONGODB_URI)


class ProductController(BaseController):
    super.__init__

    def __init__(self, db_client: AsyncIOMotorClient):
        self.size_scaled = 1048576
        self.db = db_client["products_db"]
        self.collection: AsyncIOMotorCollection = self.db["products"]

    def validate_uploaded_image(self, image: UploadFile):
        if not image.content_type.startswith("image/"):
            return False, "Upload images only"
        if image.size > app_settings.FILE_MAX_SIZE * self.size_scaled:
            return False, "file_size_exeeded"
        return True, "file_validation_success"

    def generate_unique_filename(self, file_extension):
        unique_filename = f"{ObjectId()}{file_extension}"
        return unique_filename

    async def create_product(
        self,
        title: str,
        stock: int,
        price: float,
        images: List[UploadFile],
        request: Request,
        description: Optional[str] = None,
        discount: Optional[float] = 0.0,
    ) -> dict:
        try:
            existing_product = await self.collection.find_one({"title": title})
            if existing_product:
                return {"signal": "product_already_exits"}
            BASE_DIR = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "products")
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            # Loop in uploaded images to validate
            images_url = []
            for image in images:
                valid_file, signal = self.validate_uploaded_image(image)
                if not valid_file:
                    return {"signal": signal}
                file_extension = os.path.splitext(image.filename)[1]
                unique_filename = self.generate_unique_filename(file_extension)
                file_path = os.path.join(UPLOAD_DIR, unique_filename)
                base_url = str(request.base_url)
                image_url = f"{base_url}uploads/products/{unique_filename}"
                images_url.append(image_url)
                await image.seek(0)
                content = await image.read()

                with open(file_path, "wb") as buffer:
                    buffer.write(content)

            product_data = {
                "title": title,
                "price": price,
                "description": description,
                "discount": discount,
                "stock": stock,
                "images": images_url,
            }

            result = await self.collection.insert_one(product_data)
            product_data["_id"] = str(result.inserted_id)

            return product_data

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to create product: {str(e)}"
            )

    async def get_product_by_category(
        self, category: str, skip: int = 0, limit: int = 10
    ):
        try:
            products = (
                await self.collection.find({"category": category})
                .skip(skip)
                .limit(limit)
                .to_list(length=limit)
            )
            for product in products:
                product["id"] = str(product["_id"])
                del product["_id"]
            return products
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to fetch products: {str(e)}"
            )

    async def get_product_by_id(self, product_id: str) -> dict:
        """Get a product by ID"""
        try:
            if not ObjectId.is_valid(product_id):
                raise HTTPException(status_code=400, detail="Invalid ObjectId format")

            product_oid = ObjectId(product_id)
            product = await self.collection.find_one({"_id": product_oid})

            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            product["id"] = str(product["_id"])
            del product["_id"]
            # -------------------------------

            return product
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error fetching product: {str(e)}"
            )

    async def get_all_products(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """Get all products with pagination"""
        try:
            products = (
                await self.collection.find()
                .skip(skip)
                .limit(limit)
                .to_list(length=limit)
            )
            for product in products:
                product["id"] = str(product["_id"])
                del product["_id"]
            return products
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to fetch products: {str(e)}"
            )

    async def update_product(
        self,
        request,
        product_id: str,
        title: Optional[str] = None,
        price: Optional[float] = None,
        description: Optional[str] = None,
        discount: Optional[float] = None,
        stock: Optional[int] = None,
        images: Optional[List[UploadFile]] = None,
    ) -> dict:
        """Update Product"""
        try:
            if not ObjectId.is_valid(product_id):
                raise HTTPException(status_code=400, detail="Invalid ObjectId format")

            product_oid = ObjectId(product_id)

            update_data = {}
            if title is not None:
                update_data["title"] = title
            if price is not None:
                update_data["price"] = price
            if description is not None:
                update_data["description"] = description
            if discount is not None:
                update_data["discount"] = discount
            if stock is not None:
                update_data["stock"] = stock

            if images:
                saved_images_urls = []

                BASE_DIR = os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
                UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "products")
                os.makedirs(UPLOAD_DIR, exist_ok=True)

                for image in images:
                    valid_file, signal = self.validate_uploaded_image(image)
                    if not valid_file:
                        return {"signal": signal}

                    file_extension = os.path.splitext(image.filename)[1]
                    unique_filename = self.generate_unique_filename(file_extension)
                    file_path = os.path.join(UPLOAD_DIR, unique_filename)

                    await image.seek(0)
                    content = await image.read()

                    with open(file_path, "wb") as buffer:
                        buffer.write(content)

                    base_url = str(request.base_url)
                    image_url = f"{base_url}uploads/products/{unique_filename}"
                    saved_images_urls.append(image_url)

                update_data["images"] = saved_images_urls

            if not update_data:
                raise HTTPException(
                    status_code=400, detail="No data provided for update"
                )

            result = await self.collection.find_one_and_update(
                {"_id": product_oid},
                {"$set": update_data},
                return_document=ReturnDocument.AFTER,
            )

            if not result:
                raise HTTPException(status_code=404, detail="Product not found")

            result["id"] = str(result["_id"])
            del result["_id"]

            return result

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to update product: {str(e)}"
            )

    async def delete_product(self, product_id: str) -> dict:
        """Delete a product by ID"""
        try:
            if not ObjectId.is_valid(product_id):
                raise HTTPException(status_code=400, detail="Invalid ObjectId format")

            product_oid = ObjectId(product_id)
            result = await self.collection.find_one_and_delete({"_id": product_oid})

            if not result:
                raise HTTPException(status_code=404, detail="Product not found")

            result["id"] = str(result["_id"])  
            del result["_id"]  
            # --------------------------------------------

            return {"message": "Product deleted successfully", "product": result}

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to delete product: {str(e)}"
            )

    async def search_products(
        self, query: str, skip: int = 0, limit: int = 10
    ) -> List[dict]:
        """Search products by title or description"""
        try:
            search_filter = {
                "$or": [
                    {"title": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}},
                ]
            }
            products = (
                await self.collection.find(search_filter)
                .skip(skip)
                .limit(limit)
                .to_list(length=limit)
            )
            for product in products:
                product["id"] = str(product["_id"])
            return products
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Search failed: {str(e)}")

    async def filter_by_price(
        self,
        min_price: int = 0,
        max_price: int = 999999,
        skip: int = 0,
        limit: int = 10,
    ) -> List[dict]:
        """Filter products by price range"""
        try:
            price_filter = {"price": {"$gte": min_price, "$lte": max_price}}
            products = (
                await self.collection.find(price_filter)
                .skip(skip)
                .limit(limit)
                .to_list(length=limit)
            )
            for product in products:
                product["id"] = str(product["_id"])
            return products
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Filter failed: {str(e)}")
