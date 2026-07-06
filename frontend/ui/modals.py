"""
Modal Dialogs
Forms and confirmation dialogs
"""

import flet as ft
from models import Product
from config import Colors, Sizes, Typography, Messages
from ui.components import (
    FormTextField,
    FormDropdown,
    PrimaryButton,
    DangerButton,
    Divider,
)


class ProductFormModal:
    """Product add/edit form modal"""

    def __init__(self, page: ft.Page, on_save=None):
        self.page = page
        self.on_save = on_save
        self.is_adding = True

        # Form fields
        self.product_id_field = FormTextField("Product ID", width=180)
        self.product_name_field = FormTextField("Product Name", width=180)
        self.price_field = FormTextField("Price", width=75)
        self.quantity_field = FormTextField("Quantity", width=75)

        self.category_dropdown = FormDropdown(
            "Category",
            ["Electronics", "Clothing", "Books", "Home & Garden"],
            value="Electronics",
            width=180,
        )

        self.status_dropdown = FormDropdown(
            "Status",
            ["In Stock", "Low Stock", "Out of Stock"],
            value="In Stock",
            width=180,
        )

        self.modal_title = ft.Text(
            "Add New Product",
            size=Typography.TITLE,
            weight=Typography.WEIGHT_SEMIBOLD,
            color=Colors.TEXT_PRIMARY,
        )

        # Create modal container
        self._create_modal()

    def _create_modal(self):
        """Create modal dialog structure"""
        self.modal_container = ft.Container(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Header
                        ft.Row(
                            controls=[
                                self.modal_title,
                                ft.IconButton(
                                    ft.Icons.CLOSE, icon_size=20, on_click=self._close
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Divider(),
                        # Form fields
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[self.product_id_field, self.price_field],
                                    spacing=10,
                                ),
                                ft.Row(
                                    controls=[
                                        self.product_name_field,
                                        self.quantity_field,
                                    ],
                                    spacing=10,
                                ),
                                ft.Column(
                                    controls=[
                                        self.category_dropdown,
                                        self.status_dropdown,
                                    ],
                                    spacing=10,
                                ),
                            ],
                            spacing=Sizes.PADDING,
                        ),
                        Divider(),
                        # Buttons
                        ft.Row(
                            controls=[
                                PrimaryButton("Save", width=140, on_click=self._save),
                                ft.OutlinedButton(
                                    "Cancel",
                                    width=110,
                                    height=Sizes.BUTTON_HEIGHT,
                                    on_click=self._close,
                                ),
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=Sizes.PADDING,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=Sizes.PADDING_XL,
                bgcolor=Colors.BG_SECONDARY,
                border_radius=Sizes.BORDER_RADIUS_LARGE,
                width=420,
            ),
            alignment="center",
            bgcolor="rgba(0, 0, 0, 0.4)",
            visible=False,
        )

    def open_add(self, product_id: str):
        """Open modal for adding a new product"""
        self.is_adding = True
        self.modal_title.value = "Add New Product"
        self.product_id_field.value = product_id
        self.product_name_field.value = ""
        self.category_dropdown.value = "Electronics"
        self.price_field.value = ""
        self.quantity_field.value = ""
        self.status_dropdown.value = "In Stock"

        self.product_id_field.read_only = True

        self._show()

    def open_edit(self, product: Product):
        """Open modal for editing a product"""
        self.is_adding = False
        self.modal_title.value = "Edit Product"
        self.product_id_field.value = product.id
        self.product_name_field.value = product.name
        self.category_dropdown.value = product.category
        self.price_field.value = str(product.price)
        self.quantity_field.value = str(product.quantity)
        self.status_dropdown.value = product.status

        self.product_id_field.read_only = True

        self._show()

    def _show(self):
        """Show modal"""
        self.modal_container.visible = True
        self.modal_container.update()

    def _close(self, e):
        """Close modal"""
        self.modal_container.visible = False
        self.modal_container.update()

    def _save(self, e):
        """Save form data"""
        form_data = {
            "id": self.product_id_field.value,
            "name": self.product_name_field.value,
            "category": self.category_dropdown.value,
            "price": self.price_field.value,
            "quantity": self.quantity_field.value,
            "status": self.status_dropdown.value,
        }

        if self.on_save and self.on_save(form_data):
            self._close(None)


class ConfirmDialog:
    """Confirmation dialog"""

    def __init__(self, title: str, message: str, on_confirm=None):
        self.dialog = ft.AlertDialog(
            title=ft.Text(title, size=Typography.TITLE),
            content=ft.Text(message, size=Typography.BODY),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self._close(e)),
                ft.TextButton("Confirm", on_click=self._handle_confirm(on_confirm)),
            ],
        )
        self.on_confirm = on_confirm

    def _handle_confirm(self, callback):
        """Handle confirmation callback"""

        def handler(e):
            if callback:
                callback(e)
            self._close(e)

        return handler

    def _close(self, e):
        """Close dialog"""
        self.dialog.open = False

    def show(self, page: ft.Page):
        """Show dialog on page"""
        page.dialog = self.dialog
        self.dialog.open = True
        page.update()
