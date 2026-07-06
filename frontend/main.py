"""
Product Management CRUD Application - Main Entry Point
Organized modular structure for better maintainability
"""

import flet as ft
from ui.pages import ProductManagementPage


def main(page: ft.Page):
    page.title = "Product Management System"
    page.window_width = 1400
    page.window_height = 900
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f8f9fa"

    # Initialize and display the product management page
    product_page = ProductManagementPage(page)
    page.add(product_page.build())


if __name__ == "__main__":
    ft.run(main)
