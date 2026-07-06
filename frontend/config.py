"""
Configuration and Constants
Centralized styling and app configuration
"""


# Colors
class Colors:
    """Color palette"""

    # Primary
    PRIMARY = "#3498db"
    PRIMARY_DARK = "#2980b9"

    # Backgrounds
    BG_PRIMARY = "#f8f9fa"
    BG_SECONDARY = "#ffffff"
    BG_SIDEBAR = "#2c3e50"
    BG_SIDEBAR_ALT = "#364a5e"
    BG_HEADER_ALT = "#1a252f"

    # Status colors
    SUCCESS = "#27ae60"
    WARNING = "#d68910"
    DANGER = "#e74c3c"
    INFO = "#3498db"

    # Status backgrounds
    STATUS_SUCCESS_BG = "#d5f4e6"
    STATUS_WARNING_BG = "#fef5e7"
    STATUS_DANGER_BG = "#fadbd8"

    # Category backgrounds
    CATEGORY_ELECTRONICS_BG = "#e8f4f8"
    CATEGORY_CLOTHING_BG = "#fef5e7"
    CATEGORY_BOOKS_BG = "#ebdef0"
    CATEGORY_GARDEN_BG = "#eafaf1"

    # Text colors
    TEXT_PRIMARY = "#2c3e50"
    TEXT_SECONDARY = "#95a5a6"
    TEXT_MUTED = "#7f8c8d"
    TEXT_LIGHT = "#bdc3c7"
    TEXT_WHITE = "#ffffff"

    # Borders
    BORDER = "#e0e0e0"


class StatusColors:
    """Status-specific colors"""

    STATUS_COLOR_MAP = {
        "In Stock": Colors.SUCCESS,
        "Low Stock": Colors.WARNING,
        "Out of Stock": Colors.DANGER,
    }

    STATUS_BG_MAP = {
        "In Stock": Colors.STATUS_SUCCESS_BG,
        "Low Stock": Colors.STATUS_WARNING_BG,
        "Out of Stock": Colors.STATUS_DANGER_BG,
    }

    @staticmethod
    def get_status_color(status: str) -> str:
        return StatusColors.STATUS_COLOR_MAP.get(status, Colors.TEXT_MUTED)

    @staticmethod
    def get_status_bg_color(status: str) -> str:
        return StatusColors.STATUS_BG_MAP.get(status, Colors.BG_SECONDARY)


class CategoryColors:
    """Category-specific colors"""

    COLOR_MAP = {
        "Electronics": Colors.INFO,
        "Clothing": Colors.WARNING,
        "Books": "#8e44ad",
        "Home & Garden": "#16a085",
    }

    BG_COLOR_MAP = {
        "Electronics": Colors.CATEGORY_ELECTRONICS_BG,
        "Clothing": Colors.CATEGORY_CLOTHING_BG,
        "Books": Colors.CATEGORY_BOOKS_BG,
        "Home & Garden": Colors.CATEGORY_GARDEN_BG,
    }

    @staticmethod
    def get_color(category: str) -> str:
        return CategoryColors.COLOR_MAP.get(category, Colors.TEXT_MUTED)

    @staticmethod
    def get_bg_color(category: str) -> str:
        return CategoryColors.BG_COLOR_MAP.get(category, Colors.BG_SECONDARY)


# Sizes
class Sizes:
    """Size constants"""

    SIDEBAR_WIDTH = 100
    HEADER_HEIGHT = 70
    BUTTON_HEIGHT = 40
    BUTTON_SMALL_HEIGHT = 28

    # Border radius
    BORDER_RADIUS_SMALL = 4
    BORDER_RADIUS = 6
    BORDER_RADIUS_LARGE = 8

    # Padding
    PADDING_SMALL = 10
    PADDING = 15
    PADDING_LARGE = 20
    PADDING_XL = 25


# Typography
class Typography:
    """Font sizes and weights"""

    TITLE_LARGE = 24
    TITLE = 18
    SUBTITLE = 14
    BODY = 13
    BODY_SMALL = 12
    CAPTION = 11

    WEIGHT_NORMAL = "normal"
    WEIGHT_SEMIBOLD = "w600"
    WEIGHT_BOLD = "w700"


# Icons
class Icons:
    """Icon mappings"""

    DASHBOARD = "📊"
    PRODUCTS = "📦"
    CATEGORIES = "📂"
    ANALYTICS = "📈"
    SETTINGS = "⚙️"
    SEARCH = "🔍"
    EDIT = "✏️"
    DELETE = "🗑️"
    ADD = "+"
    CHECK = "✓"
    CLOSE = "×"


# Messages
class Messages:
    """App messages"""

    # Success
    PRODUCT_ADDED = "Product added successfully"
    PRODUCT_UPDATED = "Product updated successfully"
    PRODUCT_DELETED = "Product deleted"

    # Errors
    FILL_ALL_FIELDS = "Please fill all fields"
    INVALID_PRICE = "Price must be a number"
    INVALID_QUANTITY = "Quantity must be an integer"
    PRODUCT_EXISTS = "Product already exists"

    # Confirmations
    CONFIRM_DELETE = "Are you sure you want to delete this product?"
    CONFIRM_DELETE_TITLE = "Delete Product"
