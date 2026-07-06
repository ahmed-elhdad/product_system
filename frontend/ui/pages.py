"""
Page Layouts
Main page structure and layout composition
"""

import flet as ft
from models import ProductManager, Product
from config import Colors, Sizes, Typography, Messages
from ui.components import (
    HeaderTitle,
    SearchBar,
    PrimaryButton,
    SuccessButton,
    DangerButton,
    CategoryButton,
    NavButton,
    StatusBadge,
    CategoryBadge,
    PriceText,
    FormTextField,
    FormDropdown,
    StatsCard,
    ActionRow,
    SidebarSection,
    Divider,
)
from ui.modals import ProductFormModal, ConfirmDialog


class ProductManagementPage:
    """Main product management page"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.product_manager = ProductManager()
        self.selected_category = "Al Products"
        self.editing_product = None

        # Initialize UI components
        self.search_field = SearchBar(on_change=self.on_search_change)
        self.product_table = self._create_product_table()
        self.stats_total = StatsCard("Total Products")
        self.stats_in_stock = StatsCard("In Stock")
        self.stats_low_stock = StatsCard("Low Stock")
        self.stats_out = StatsCard("Out of Stock")

        self.form_modal = ProductFormModal(self.page, on_save=self.save_product)
        self.category_buttons = []

    def _create_product_table(self) -> ft.DataTable:
        """Create product data table"""
        return ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text(
                        "Product ID",
                        size=Typography.BODY_SMALL,
                        weight=Typography.WEIGHT_SEMIBOLD,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Product Name",
                        size=Typography.BODY_SMALL,
                        weight=Typography.WEIGHT_SEMIBOLD,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Category",
                        size=Typography.BODY_SMALL,
                        weight=Typography.WEIGHT_SEMIBOLD,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Price",
                        size=Typography.BODY_SMALL,
                        weight=Typography.WEIGHT_SEMIBOLD,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Quantity",
                        size=Typography.BODY_SMALL,
                        weight=Typography.WEIGHT_SEMIBOLD,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Status",
                        size=Typography.BODY_SMALL,
                        weight=Typography.WEIGHT_SEMIBOLD,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Actions",
                        size=Typography.BODY_SMALL,
                        weight=Typography.WEIGHT_SEMIBOLD,
                    )
                ),
            ],
            rows=[],
            border_radius=Sizes.BORDER_RADIUS,
        )

    def _create_sidebar(self) -> ft.Container:
        """Create sidebar navigation"""
        # Navigation buttons (compact version)
        nav_buttons = [
            NavButton("📊 Dashboard", is_active=True),
            NavButton("📦 Products"),
            NavButton("📂 Categories"),
            NavButton("📈 Analytics"),
        ]

        # Category filter buttons
        category_buttons = []
        for i, category in enumerate(self.product_manager.categories):
            is_active = category == "All Products"
            btn = CategoryButton(
                f"{'✓' if is_active else ''} {category}",
                data=category,
                is_active=is_active,
                on_click=lambda e: self.filter_by_category(e.control.data),
            )
            category_buttons.append(btn)

        self.category_buttons = category_buttons

        sidebar = ft.Container(
            content=ft.Column(
                controls=[
                    # Logo
                    ft.Container(
                        content=ft.Text(
                            "Product Hub",
                            size=Typography.TITLE,
                            weight=Typography.WEIGHT_NORMAL,
                            color=Colors.TEXT_WHITE,
                        ),
                        padding=Sizes.PADDING_SMALL,
                        bgcolor=Colors.BG_HEADER_ALT,
                        height=Sizes.HEADER_HEIGHT,
                        alignment="center_left",
                    ),
                    Divider(),
                    # Navigation
                    ft.Container(
                        content=ft.Column(controls=nav_buttons, spacing=2),
                        padding=5,
                    ),
                    # Category Filter Section
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "FILTERS BY CATEGORY",
                                    size=10,
                                    weight="w600",
                                    color=Colors.TEXT_LIGHT,
                                ),
                                ft.Column(controls=category_buttons, spacing=2),
                            ],
                            spacing=8,
                        ),
                        padding=10,
                        bgcolor=Colors.BG_SIDEBAR_ALT,
                    ),
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            ),
            width=300,
            bgcolor=Colors.BG_SIDEBAR,
            padding=0,
            expand=False,
        )

        return sidebar

    def _create_header(self) -> ft.Container:
        """Create page header"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    HeaderTitle("All Products"),
                    ft.Row(
                        controls=[
                            self.search_field,
                            PrimaryButton(
                                "+ Add Product",
                                width=130,
                                on_click=self.show_add_product_modal,
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=Sizes.PADDING_LARGE,
            bgcolor=Colors.BG_SECONDARY,
            border=ft.Border.only(bottom=ft.BorderSide(1, Colors.BORDER)),
        )

    def _create_content(self) -> ft.Container:
        """Create main content area"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self.product_table,
                        expand=True,
                        padding=Sizes.PADDING_LARGE,
                    ),
                    Divider(),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                self.stats_total,
                                self.stats_in_stock,
                                self.stats_low_stock,
                                self.stats_out,
                            ],
                            spacing=30,
                        ),
                        padding=Sizes.PADDING_LARGE,
                        bgcolor=Colors.BG_SECONDARY,
                    ),
                ],
                spacing=0,
            ),
            expand=True,
            bgcolor=Colors.BG_SECONDARY,
        )

    def _update_product_table(self):
        """Update product table with current data"""
        # Get filtered products
        filtered_products = self.product_manager.filter_by_category(
            self.selected_category
        )

        # Apply search
        search_text = self.search_field.value.lower() if self.search_field.value else ""
        if search_text:
            filtered_products = self.product_manager.search_products(search_text)
            if self.selected_category != "All Products":
                filtered_products = [
                    p for p in filtered_products if p.category == self.selected_category
                ]

        # Clear table rows
        self.product_table.rows.clear()

        # Add product rows
        for product in filtered_products:
            self.product_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                product.id,
                                size=Typography.BODY,
                                color=Colors.TEXT_SECONDARY,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                product.name,
                                size=Typography.BODY,
                                color=Colors.TEXT_PRIMARY,
                            )
                        ),
                        ft.DataCell(CategoryBadge(product.category)),
                        ft.DataCell(PriceText(product.price)),
                        ft.DataCell(
                            ft.Text(
                                str(product.quantity),
                                size=Typography.BODY,
                                color=Colors.TEXT_PRIMARY,
                            )
                        ),
                        ft.DataCell(StatusBadge(product.status)),
                        ft.DataCell(
                            ActionRow(
                                on_edit=lambda e, p=product: self.show_edit_modal(p),
                                on_delete=lambda e, p=product: self.show_delete_confirm(
                                    p
                                ),
                            )
                        ),
                    ]
                )
            )

        # Update statistics
        stats = self.product_manager.get_statistics(filtered_products)
        self.stats_total.value = f"Total Products: {stats['total']}"
        self.stats_in_stock.value = f"In Stock: {stats['in_stock']}"
        self.stats_low_stock.value = f"Low Stock: {stats['low_stock']}"
        self.stats_out.value = f"Out of Stock: {stats['out_of_stock']}"

        # Update UI
        self.product_table.update()
        self.stats_total.update()
        self.stats_in_stock.update()
        self.stats_low_stock.update()
        self.stats_out.update()

    def filter_by_category(self, category: str):
        """Filter products by category"""
        self.selected_category = category

        # Update button styles
        for btn in self.category_buttons:
            if btn.data == category:
                btn.label = f"✓ {category}"
                btn.style.color = Colors.PRIMARY
                btn.style.text_style.weight = Typography.WEIGHT_SEMIBOLD
            else:
                btn.label = btn.data
                btn.style.color = Colors.TEXT_SECONDARY
                btn.style.text_style.weight = Typography.WEIGHT_NORMAL
            btn.update()

        self._update_product_table()

    def on_search_change(self, e):
        """Handle search input change"""
        self._update_product_table()

    def show_add_product_modal(self, e):
        """Show add product modal"""
        self.editing_product = None
        new_id = self.product_manager.generate_product_id()
        self.form_modal.open_add(new_id)

    def show_edit_modal(self, product: Product):
        """Show edit product modal"""
        self.editing_product = product
        self.form_modal.open_edit(product)

    def show_delete_confirm(self, product: Product):
        """Show delete confirmation dialog"""

        def on_confirm(e):
            self.product_manager.delete_product(product.id)
            self.show_snackbar(Messages.PRODUCT_DELETED, Colors.DANGER)
            self._update_product_table()

        dialog = ConfirmDialog(
            title=Messages.CONFIRM_DELETE_TITLE,
            message=f"{Messages.CONFIRM_DELETE}\n\n'{product.name}'",
            on_confirm=on_confirm,
        )
        dialog.show(self.page)

    def save_product(self, form_data: dict):
        """Save product (add or update)"""
        try:
            # Validate data
            if not all(
                [
                    form_data.get("name"),
                    form_data.get("price"),
                    form_data.get("quantity"),
                ]
            ):
                self.show_snackbar(Messages.FILL_ALL_FIELDS, Colors.WARNING)
                return False

            try:
                price = float(form_data["price"])
                quantity = int(form_data["quantity"])
            except ValueError:
                msg = (
                    Messages.INVALID_PRICE
                    if isinstance(form_data["price"], str)
                    else Messages.INVALID_QUANTITY
                )
                self.show_snackbar(msg, Colors.WARNING)
                return False

            if self.editing_product:
                # Update existing product
                self.product_manager.update_product(
                    self.editing_product.id,
                    {
                        "name": form_data["name"],
                        "category": form_data["category"],
                        "price": price,
                        "quantity": quantity,
                        "status": form_data["status"],
                    },
                )
                self.show_snackbar(Messages.PRODUCT_UPDATED, Colors.SUCCESS)
            else:
                # Add new product
                new_product = Product(
                    id=form_data["id"],
                    name=form_data["name"],
                    category=form_data["category"],
                    price=price,
                    quantity=quantity,
                    status=form_data["status"],
                )
                if not self.product_manager.add_product(new_product):
                    self.show_snackbar(Messages.PRODUCT_EXISTS, Colors.WARNING)
                    return False
                self.show_snackbar(Messages.PRODUCT_ADDED, Colors.SUCCESS)

            self._update_product_table()
            return True

        except Exception as ex:
            self.show_snackbar(f"Error: {str(ex)}", Colors.DANGER)
            return False

    def show_snackbar(self, message: str, bg_color: str = None):
        """Show notification snackbar"""
        snack = ft.SnackBar(
            ft.Text(message, color=Colors.TEXT_WHITE),
            bgcolor=bg_color or Colors.SUCCESS,
            expand=True,
        )
        self.page.snack_bar = snack
        snack.open = True
        self.page.update()

    def build(self) -> ft.Row:
        """Build the complete page layout"""
        return ft.Row(
            controls=[
                self._create_sidebar(),
                ft.Column(
                    controls=[
                        self._create_header(),
                        self._create_content(),
                    ],
                    expand=True,
                    spacing=0,
                ),
            ],
            spacing=0,
            expand=True,
        )
