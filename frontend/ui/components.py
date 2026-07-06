"""
Reusable UI Components
Custom components built on top of Flet
"""

import flet as ft
from config import Colors, Sizes, Typography, StatusColors, CategoryColors


class PrimaryButton(ft.ElevatedButton):
    """Primary action button"""

    def __init__(
        self,
        text: str,
        width: int = None,
        height: int = Sizes.BUTTON_HEIGHT,
        on_click=None,
    ):
        super().__init__(
            content=text,
            width=width,
            height=height,
            style=ft.ButtonStyle(
                bgcolor=Colors.PRIMARY,
                color=Colors.TEXT_WHITE,
                text_style=ft.TextStyle(
                    size=Typography.BODY, weight=Typography.WEIGHT_SEMIBOLD
                ),
            ),
            on_click=on_click,
        )


class DangerButton(ft.ElevatedButton):
    """Danger action button (delete)"""

    def __init__(
        self,
        text: str,
        width: int = None,
        height: int = Sizes.BUTTON_HEIGHT,
        on_click=None,
    ):
        super().__init__(
            text=text,
            width=width,
            height=height,
            style=ft.ButtonStyle(
                bgcolor=Colors.DANGER,
                color=Colors.TEXT_WHITE,
                text_style=ft.TextStyle(
                    size=Typography.BODY, weight=Typography.WEIGHT_SEMIBOLD
                ),
            ),
            on_click=on_click,
        )


class SuccessButton(ft.ElevatedButton):
    """Success action button (edit)"""

    def __init__(
        self,
        text: str,
        width: int = None,
        height: int = Sizes.BUTTON_HEIGHT,
        on_click=None,
    ):
        super().__init__(
            text=text,
            width=width,
            height=height,
            style=ft.ButtonStyle(
                bgcolor=Colors.SUCCESS,
                color=Colors.TEXT_WHITE,
                text_style=ft.TextStyle(
                    size=Typography.BODY, weight=Typography.WEIGHT_SEMIBOLD
                ),
            ),
            on_click=on_click,
        )


class StatusBadge(ft.Container):
    """Status indicator badge"""

    def __init__(self, status: str):
        color = StatusColors.get_status_color(status)
        bg_color = StatusColors.get_status_bg_color(status)

        super().__init__(
            content=ft.Text(
                status,
                size=Typography.CAPTION,
                weight=Typography.WEIGHT_SEMIBOLD,
                color=color,
            ),
            bgcolor=bg_color,
            padding=Sizes.PADDING_SMALL,
            border_radius=Sizes.BORDER_RADIUS_SMALL,
            width=80,
        )


class CategoryBadge(ft.Container):
    """Category indicator badge"""

    def __init__(self, category: str):
        color = CategoryColors.get_color(category)
        bg_color = CategoryColors.get_bg_color(category)

        super().__init__(
            content=ft.Text(
                category,
                size=Typography.CAPTION,
                weight=Typography.WEIGHT_SEMIBOLD,
                color=color,
            ),
            bgcolor=bg_color,
            padding=Sizes.PADDING_SMALL,
            border_radius=Sizes.BORDER_RADIUS_SMALL,
            width=95,
        )


class PriceText(ft.Text):
    """Price display text"""

    def __init__(self, price: float):
        super().__init__(
            f"${price:.2f}",
            size=Typography.BODY,
            weight=Typography.WEIGHT_SEMIBOLD,
            color=Colors.SUCCESS,
        )


class SearchBar(ft.TextField):
    """Search input field"""

    def __init__(self, on_change=None, width: int = 180):
        super().__init__(
            label="Search products...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=Sizes.BORDER_RADIUS,
            width=width,
            height=Sizes.BUTTON_HEIGHT,
            on_change=on_change,
        )


class NavButton(ft.TextButton):
    """Navigation button"""

    def __init__(self, label: str, is_active: bool = False, on_click=None):
        super().__init__(
            label,
            style=ft.ButtonStyle(
                color=Colors.PRIMARY if is_active else Colors.TEXT_SECONDARY,
                text_style=ft.TextStyle(
                    size=11,
                    weight=(
                        Typography.WEIGHT_SEMIBOLD
                        if is_active
                        else Typography.WEIGHT_NORMAL
                    ),
                ),
            ),
            on_click=on_click,
        )


class CategoryButton(ft.TextButton):
    """Category filter button"""

    def __init__(self, label: str, data: str, is_active: bool = False, on_click=None):
        super().__init__(
            label,
            data=data,
            style=ft.ButtonStyle(
                color=Colors.PRIMARY if is_active else Colors.TEXT_SECONDARY,
                text_style=ft.TextStyle(
                    size=11,
                    weight=(
                        Typography.WEIGHT_SEMIBOLD
                        if is_active
                        else Typography.WEIGHT_NORMAL
                    ),
                ),
            ),
            on_click=on_click,
        )


class FormTextField(ft.TextField):
    """Standard form text field"""

    def __init__(self, label: str, width: int = 180):
        super().__init__(
            label=label,
            width=width,
            height=Sizes.BUTTON_HEIGHT,
            border_radius=Sizes.BORDER_RADIUS,
        )


class FormDropdown(ft.Dropdown):
    """Standard form dropdown"""

    def __init__(self, label: str, options: list, value: str = None, width: int = 180):
        super().__init__(
            label=label,
            options=[ft.dropdown.Option(opt) for opt in options],
            value=value or options[0],
            width=width,
            height=Sizes.BUTTON_HEIGHT,
        )


class StatsCard(ft.Text):
    """Statistics card text"""

    def __init__(self, label: str, value: int = 0):
        super().__init__(
            f"{label}: {value}",
            size=Typography.BODY_SMALL,
            weight=Typography.WEIGHT_SEMIBOLD,
            color=Colors.TEXT_MUTED,
        )


class ActionRow(ft.Row):
    """Action buttons row for table"""

    def __init__(self, on_edit=None, on_delete=None):
        super().__init__(
            controls=[
                SuccessButton(
                    "Edit", width=40, height=Sizes.BUTTON_SMALL_HEIGHT, on_click=on_edit
                ),
                DangerButton(
                    "Del",
                    width=40,
                    height=Sizes.BUTTON_SMALL_HEIGHT,
                    on_click=on_delete,
                ),
            ],
            spacing=5,
            expand=True,
        )


class SidebarSection(ft.Container):
    """Sidebar section container"""

    def __init__(self, title: str, content: ft.Column):
        super().__init__(
            content=ft.Column(
                controls=[
                    ft.Text(
                        title,
                        size=Typography.BODY_SMALL,
                        weight=Typography.WEIGHT_SEMIBOLD,
                        color=Colors.TEXT_LIGHT,
                    ),
                    content,
                ],
                spacing=Sizes.PADDING,
            ),
            width=240,
            expand=False,
            padding=Sizes.PADDING_SMALL,
            bgcolor=Colors.BG_SIDEBAR_ALT,
        )


class HeaderTitle(ft.Text):
    """Page header title"""

    def __init__(self, title: str):
        super().__init__(
            title,
            size=Typography.TITLE_LARGE,
            weight=Typography.WEIGHT_SEMIBOLD,
            color=Colors.TEXT_PRIMARY,
        )


class Divider(ft.Divider):
    """Standard divider"""

    def __init__(self):
        super().__init__(height=1, color=Colors.BORDER)
