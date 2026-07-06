"""
Utility Functions and Helpers
Common utility functions used across the application
"""

from datetime import datetime
from typing import Any, List, Dict
import json


class ValidationHelper:
    """Input validation helpers"""

    @staticmethod
    def is_valid_price(price: Any) -> bool:
        """Check if price is a valid number"""
        try:
            float(price)
            return float(price) > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_valid_quantity(quantity: Any) -> bool:
        """Check if quantity is a valid integer"""
        try:
            int(quantity)
            return int(quantity) >= 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_valid_product_name(name: str) -> bool:
        """Check if product name is valid"""
        return isinstance(name, str) and len(name.strip()) > 0

    @staticmethod
    def validate_product_data(data: dict) -> tuple[bool, str]:
        """Validate complete product data"""
        if not data.get("name") or not isinstance(data["name"], str):
            return False, "Invalid product name"

        if not ValidationHelper.is_valid_price(data.get("price")):
            return False, "Invalid price"

        if not ValidationHelper.is_valid_quantity(data.get("quantity")):
            return False, "Invalid quantity"

        if not data.get("category"):
            return False, "Category is required"

        if not data.get("status"):
            return False, "Status is required"

        return True, "Valid"


class FormattingHelper:
    """Data formatting helpers"""

    @staticmethod
    def format_price(price: float) -> str:
        """Format price as currency"""
        return f"${price:.2f}"

    @staticmethod
    def format_quantity(quantity: int) -> str:
        """Format quantity with thousand separator"""
        return f"{quantity:,}"

    @staticmethod
    def format_timestamp(timestamp: datetime = None) -> str:
        """Format timestamp"""
        if timestamp is None:
            timestamp = datetime.now()
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def truncate_text(text: str, length: int = 50) -> str:
        """Truncate text to specified length"""
        if len(text) > length:
            return text[: length - 3] + "..."
        return text


class ExportHelper:
    """Data export helpers"""

    @staticmethod
    def export_to_csv(products: List[dict], filename: str = "products.csv") -> bool:
        """Export products to CSV"""
        try:
            import csv

            with open(filename, "w", newline="") as csvfile:
                if not products:
                    return False

                fieldnames = products[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(products)

            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False

    @staticmethod
    def export_to_json(products: List[dict], filename: str = "products.json") -> bool:
        """Export products to JSON"""
        try:
            with open(filename, "w") as jsonfile:
                json.dump(products, jsonfile, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False

    @staticmethod
    def import_from_json(filename: str) -> List[dict]:
        """Import products from JSON"""
        try:
            with open(filename, "r") as jsonfile:
                return json.load(jsonfile)
        except Exception as e:
            print(f"Error importing from JSON: {e}")
            return []


class SearchHelper:
    """Search and filtering helpers"""

    @staticmethod
    def fuzzy_search(query: str, items: List[str]) -> List[str]:
        """Simple fuzzy search"""
        query = query.lower()
        return [item for item in items if query in item.lower()]

    @staticmethod
    def search_by_field(
        query: str, objects: List[dict], fields: List[str]
    ) -> List[dict]:
        """Search objects by specific fields"""
        query = query.lower()
        return [
            obj
            for obj in objects
            if any(query in str(obj.get(field, "")).lower() for field in fields)
        ]


class SortingHelper:
    """Sorting helpers"""

    @staticmethod
    def sort_products_by_price(
        products: List[dict], reverse: bool = False
    ) -> List[dict]:
        """Sort products by price"""
        return sorted(products, key=lambda x: x.get("price", 0), reverse=reverse)

    @staticmethod
    def sort_products_by_quantity(
        products: List[dict], reverse: bool = False
    ) -> List[dict]:
        """Sort products by quantity"""
        return sorted(products, key=lambda x: x.get("quantity", 0), reverse=reverse)

    @staticmethod
    def sort_products_by_name(
        products: List[dict], reverse: bool = False
    ) -> List[dict]:
        """Sort products by name"""
        return sorted(products, key=lambda x: x.get("name", ""), reverse=reverse)


class StatisticsHelper:
    """Statistics calculation helpers"""

    @staticmethod
    def calculate_total_value(products: List[dict]) -> float:
        """Calculate total inventory value"""
        return sum(p.get("price", 0) * p.get("quantity", 0) for p in products)

    @staticmethod
    def calculate_average_price(products: List[dict]) -> float:
        """Calculate average product price"""
        if not products:
            return 0
        return sum(p.get("price", 0) for p in products) / len(products)

    @staticmethod
    def calculate_total_quantity(products: List[dict]) -> int:
        """Calculate total quantity of all products"""
        return sum(p.get("quantity", 0) for p in products)

    @staticmethod
    def get_category_statistics(products: List[dict]) -> Dict[str, int]:
        """Get product count by category"""
        stats = {}
        for product in products:
            category = product.get("category", "Uncategorized")
            stats[category] = stats.get(category, 0) + 1
        return stats

    @staticmethod
    def get_low_stock_products(products: List[dict], threshold: int = 20) -> List[dict]:
        """Get products below stock threshold"""
        return [p for p in products if p.get("quantity", 0) < threshold]
