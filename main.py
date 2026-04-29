import flet as ft
import os
from database.connection import init_db
from views.dashboard import DashboardView
from views.members_view import MembersView
from views.payments_view import PaymentsView
from views.access_view import AccessLogView
from views.settings_view import SettingsView
from views.plans_view import PlansView
from views.access_control_view import AccessControlView
from views.reports_view import ReportsView
from views.login_view import LoginView, ROLE_PERMISSIONS

ALL_DESTINATIONS = [
    ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD,         label="Dashboard"),
    ft.NavigationRailDestination(icon=ft.Icons.PEOPLE_OUTLINED,    selected_icon=ft.Icons.PEOPLE,            label="Members"),
    ft.NavigationRailDestination(icon=ft.Icons.LIST_ALT_OUTLINED,  selected_icon=ft.Icons.LIST_ALT,          label="Plans"),
    ft.NavigationRailDestination(icon=ft.Icons.PAYMENTS_OUTLINED,  selected_icon=ft.Icons.PAYMENTS,          label="Payments"),
    ft.NavigationRailDestination(icon=ft.Icons.LOGIN,              selected_icon=ft.Icons.LOGIN,             label="Gate"),
    ft.NavigationRailDestination(icon=ft.Icons.HISTORY_OUTLINED,   selected_icon=ft.Icons.HISTORY,           label="History"),
    ft.NavigationRailDestination(icon=ft.Icons.INSERT_CHART_OUTLINED, selected_icon=ft.Icons.INSERT_CHART,   label="Reports"),
    ft.NavigationRailDestination(icon=ft.Icons.SETTINGS_OUTLINED,  selected_icon=ft.Icons.SETTINGS,         label="Settings"),
]

VIEW_BUILDERS = [
    DashboardView,
    MembersView,
    PlansView,
    PaymentsView,
    AccessControlView,
    AccessLogView,
    ReportsView,
    SettingsView,
]

def main(page: ft.Page):
    page.title = "Sports Club Management System"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1350
    page.window_height = 950
    page.padding = 0
    page.bgcolor = ft.Colors.SURFACE
    page.window.icon = "favicon.ico"

    current_role = {"value": None}

    # ── Root layout wrapper ───────────────────────────────────────────────
    root = ft.Column(expand=True)
    page.add(root)

    def show_login():
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.add(LoginView(page, on_login=on_login))
        page.update()

    def on_login(role: str):
        current_role["value"] = role
        page.clean()
        build_main_ui()

    def build_main_ui():
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        role = current_role["value"]
        allowed = ROLE_PERMISSIONS.get(role, [])

        # Map allowed tab indices to consecutive rail indices
        # allowed[i] = real tab index, rail_idx -> real tab idx
        visible_destinations = [ALL_DESTINATIONS[i] for i in allowed]
        rail_to_real = {rail_i: real_i for rail_i, real_i in enumerate(allowed)}

        content_area = ft.Container(expand=True)

        def change_view(rail_index):
            real_index = rail_to_real.get(rail_index, 0)
            content_area.content = VIEW_BUILDERS[real_index](page)
            page.update()
        def logout(e):
            current_role["value"] = None
            show_login()

        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=110,
            min_extended_width=200,
            bgcolor="#013484",
            group_alignment=-0.9,
            destinations=visible_destinations,
            on_change=lambda e: change_view(e.control.selected_index),
            leading=ft.Container(
                content=ft.Image(src="favicon-white.png", width=56, height=56, fit=ft.BoxFit.CONTAIN),
                padding=ft.Padding(0, 16, 0, 8),
                tooltip="Sports Club",
            ),
            trailing=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color=ft.Colors.WHITE70, size=20),
                        ft.Text(role.capitalize(), color=ft.Colors.WHITE70, size=11),
                    ], spacing=4),
                    padding=ft.Padding(8, 4, 8, 4),
                    tooltip=f"Signed in as: {role}",
                ),

                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color=ft.Colors.WHITE70,
                    tooltip="Logout",
                    on_click=logout,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
        )

        layout = ft.Row([rail, ft.VerticalDivider(width=1), content_area], expand=True)
        page.add(layout)
        

        
        change_view(0)

    # Start at login
    show_login()

if __name__ == "__main__":
    schema_path = os.path.join("database", "schema.sql")
    init_db(schema_path)
    ft.app(target=main, assets_dir="assets")
