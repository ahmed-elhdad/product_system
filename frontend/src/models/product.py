class Product:
    """Product data model"""

    id: str
    title: str
    category: str
    price: float
    stock: int
    status: str

    def to_dict(self):
        """Convert product to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict):
        """Create product from dictionary"""
        return Product(**data)

