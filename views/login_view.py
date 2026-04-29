import flet as ft

ROLES = {
    "admin":       "admin123",
    "cashier":     "cashier123",
    "receptionist":"recep123",
}

ROLE_PERMISSIONS = {
    "admin":       [0, 1, 2, 3, 4, 5, 6, 7],   # all tabs
    "cashier":     [0, 1, 3, 6],                 # dashboard, members, payments, reports
    "receptionist":[0, 1, 4, 5],                 # dashboard, members, gate, history
}

def LoginView(page: ft.Page, on_login):
    """
    Displays a login screen. Calls on_login(role) on success.
    """
    username_field = ft.TextField(
        label="Username",
        autofocus=True,
        width=320,
        prefix_icon=ft.Icons.PERSON,
    )
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=320,
        prefix_icon=ft.Icons.LOCK,
    )
    error_text = ft.Text("", color=ft.Colors.RED_400, size=13)

    def attempt_login(e):
        user = username_field.value.strip().lower()
        pwd  = password_field.value
        if ROLES.get(user) == pwd:
            error_text.value = ""
            on_login(user)
        else:
            error_text.value = "Invalid username or password."
            password_field.value = ""
            page.update()

    password_field.on_submit = attempt_login

    role_hints = ft.Column([
        ft.Text("Available roles (demo):", size=11, color=ft.Colors.ON_SURFACE_VARIANT),
        ft.Text("admin / admin123", size=11, color=ft.Colors.ON_SURFACE_VARIANT),
        ft.Text("cashier / cashier123", size=11, color=ft.Colors.ON_SURFACE_VARIANT),
        ft.Text("receptionist / recep123", size=11, color=ft.Colors.ON_SURFACE_VARIANT),
    ], spacing=2)

    login_card = ft.Container(
        content=ft.Column([
            ft.Image(src="favicon.png", width=72, height=72, fit=ft.BoxFit.CONTAIN),
            ft.Text("Sports Club", size=26, weight=ft.FontWeight.BOLD),
            ft.Text("Management System", size=13, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            username_field,
            password_field,
            error_text,
            ft.ElevatedButton(
                "Sign In",
                icon=ft.Icons.LOGIN,
                width=320,
                height=45,
                bgcolor="#013484",
                color=ft.Colors.WHITE,
                on_click=attempt_login,
            ),
            ft.Divider(height=12, color=ft.Colors.TRANSPARENT),
            role_hints,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10),
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        border_radius=20,
        padding=40,
        width=420,
    )

    return ft.Container(
        content=ft.Column(
            [login_card],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
        expand=True,
        alignment=ft.Alignment(0, 0),
    )
