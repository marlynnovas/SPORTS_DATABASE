import flet as ft
import os
from database.connection import init_db
from views.dashboard import DashboardView
from views.members_view import MembersView
from views.access_view import AccessLogView
from views.settings_view import SettingsView
from views.payments_view import PaymentsView

def main(page: ft.Page):
    page.title = "Sports Club Management System"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1300
    page.window_height = 900
    page.padding = 0
    page.bgcolor = ft.Colors.SURFACE

    # Current view in the content area
    content_area = ft.Container(expand=True)

    def change_view(index):
        if index == 0:
            content_area.content = DashboardView(page)
        elif index == 1:
            content_area.content = MembersView(page)
        elif index == 2:
            content_area.content = PaymentsView(page)
        elif index == 3:
            content_area.content = AccessLogView(page)
        elif index == 4:
            content_area.content = SettingsView(page)
        page.update()

    # Sidebar / Navigation Rail
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DASHBOARD_OUTLINED,
                selected_icon=ft.Icons.DASHBOARD,
                label="Dashboard",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE_OUTLINED,
                selected_icon=ft.Icons.PEOPLE,
                label="Members",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PAYMENTS_OUTLINED,
                selected_icon=ft.Icons.PAYMENTS,
                label="Payments",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.HISTORY_OUTLINED,
                selected_icon=ft.Icons.HISTORY,
                label="Access Logs",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Settings",
            ),
        ],
        on_change=lambda e: change_view(e.control.selected_index),
    )

    # App Layout
    layout = ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            content_area,
        ],
        expand=True,
    )

    page.add(layout)
    
    # Set initial view
    change_view(0)

if __name__ == "__main__":
    schema_path = os.path.join("database", "schema.sql")
    init_db(schema_path)
    ft.app(target=main)
