"""
Data Models and Business Logic
Handles product data management and validation
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Product:
    """Product data model"""

    id: str
    name: str
    category: str
    price: float
    quantity: int
    status: str

    def to_dict(self):
        """Convert product to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict):
        """Create product from dictionary"""
        return Product(**data)


class ProductManager:
    """Manages product data and operations"""

    def __init__(self):
        self.products: List[Product] = [
            Product(
                "P001", "Wireless Headphones", "Electronics", 79.99, 45, "In Stock"
            ),
            Product(
                "P002", "Premium Winter Jacket", "Clothing", 129.99, 12, "Low Stock"
            ),
            Product("P003", "Python Programming Book", "Books", 49.99, 156, "In Stock"),
            Product(
                "P004", "Indoor Plant Pot Set", "Home & Garden", 34.50, 87, "In Stock"
            ),
            Product(
                "P005", "USB-C Fast Charger", "Electronics", 24.99, 0, "Out of Stock"
            ),
        ]
        self.categories = [
            "All Products",
            "Electronics",
            "Clothing",
            "Books",
            "Home & Garden",
        ]
        self.statuses = ["In Stock", "Low Stock", "Out of Stock"]

    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self.products

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def add_product(self, product: Product) -> bool:
        """Add a new product"""
        if self.get_product_by_id(product.id):
            return False
        self.products.append(product)
        return True

    def update_product(self, product_id: str, updated_data: dict) -> bool:
        """Update an existing product"""
        product = self.get_product_by_id(product_id)
        if not product:
            return False

        product.name = updated_data.get("name", product.name)
        product.category = updated_data.get("category", product.category)
        product.price = updated_data.get("price", product.price)
        product.quantity = updated_data.get("quantity", product.quantity)
        product.status = updated_data.get("status", product.status)
        return True

    def delete_product(self, product_id: str) -> bool:
        """Delete a product"""
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        self.products.remove(product)
        return True

    def search_products(self, query: str) -> List[Product]:
        """Search products by name or ID"""
        query = query.lower()
        return [
            p for p in self.products if query in p.name.lower() or query in p.id.lower()
        ]

    def filter_by_category(self, category: str) -> List[Product]:
        """Filter products by category"""
        if category == "All Products":
            return self.products
        return [p for p in self.products if p.category == category]

    def get_statistics(self, products: List[Product]) -> dict:
        """Calculate product statistics"""
        return {
            "total": len(products),
            "in_stock": sum(1 for p in products if p.status == "In Stock"),
            "low_stock": sum(1 for p in products if p.status == "Low Stock"),
            "out_of_stock": sum(1 for p in products if p.status == "Out of Stock"),
        }

    def generate_product_id(self) -> str:
        """Generate next product ID"""
        next_num = len(self.products) + 1
        return f"P{str(next_num).zfill(3)}"
