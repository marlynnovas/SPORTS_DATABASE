import os
from dotenv import load_dotenv

load_dotenv()

import flet as ft
from database.connection import init_db

def main(page: ft.Page):
    page.title = "Sports Club Management System"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 800
    
    # Header
    header = ft.AppBar(
        leading=ft.Icon(ft.icons.SPORTS_VOLLEYBALL),
        title=ft.Text("Sports Club - Access Control & Payments"),
        bgcolor=ft.colors.SURFACE_VARIANT,
    )
    
    # Basic Navigation / Placeholder
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    header,
                    ft.Text("Dashboard - Welcome to Sports Club App!", size=30),
                    ft.ElevatedButton("Go to Members", on_click=lambda _: page.go("/members")),
                ],
            )
        )
        if page.route == "/members":
            page.views.append(
                ft.View(
                    "/members",
                    [
                        header,
                        ft.Text("Members Management", size=30),
                        ft.ElevatedButton("Back to Dashboard", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    # Initialize DB (if needed)
    schema_path = os.path.join("database", "schema.sql")
    init_db(schema_path)
    
    ft.app(target=main)
