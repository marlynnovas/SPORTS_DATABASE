import flet as ft
from services.member_service import MemberService

def DashboardView(page: ft.Page):
    member_count = MemberService.count_members()

    # ── Stat cards ─────────────────────────────────────────────────────
    def stat_card(title, value, subtitle, icon, color, bg):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, size=26, color=ft.Colors.WHITE),
                        bgcolor=color, border_radius=10, padding=10, width=48, height=48
                    ),
                    ft.Column([
                        ft.Text(value, size=28, weight=ft.FontWeight.BOLD),
                        ft.Text(title, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                    ], spacing=0, expand=True)
                ], spacing=12),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Text(subtitle, size=11, color=ft.Colors.ON_SURFACE_VARIANT),
            ], spacing=0),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=12,
            padding=18,
            expand=True
        )

    stats_row = ft.Row([
        stat_card("Total Members",   f"{member_count}", "↑ 2 this week",        ft.Icons.PEOPLE,         ft.Colors.BLUE_600, ft.Colors.BLUE_50),
        stat_card("Active Plans",    f"{member_count}", "All current",           ft.Icons.CHECK_CIRCLE,   ft.Colors.GREEN_600, ft.Colors.GREEN_50),
        stat_card("Revenue (MTD)",   "$45,200",         "↑ 12% vs last month",   ft.Icons.ATTACH_MONEY,  ft.Colors.PURPLE_600, ft.Colors.PURPLE_50),
        stat_card("Access Today",    "24",              "Last: 10:43 AM",         ft.Icons.LOGIN,         ft.Colors.ORANGE_600, ft.Colors.ORANGE_50),
        stat_card("Pending Bills",   "5",               "Due this week",          ft.Icons.RECEIPT_LONG,  ft.Colors.RED_600, ft.Colors.RED_50),
    ], spacing=12)

    # ── Recent activity table ───────────────────────────────────────────
    activity_rows = [
        ("Juan Perez",       "10:43 AM", "Monthly Basic",   "Entry", ft.Colors.GREEN,  ft.Colors.GREEN_100,  "Granted"),
        ("Maria Rodriguez",  "10:30 AM", "Yearly Premium",  "Entry", ft.Colors.GREEN,  ft.Colors.GREEN_100,  "Granted"),
        ("Pedro García",     "09:55 AM", "Quarterly",       "Entry", ft.Colors.GREEN,  ft.Colors.GREEN_100,  "Granted"),
        ("Luis Martínez",    "09:30 AM", "Monthly Basic",   "Entry", ft.Colors.RED,    ft.Colors.RED_100,    "Denied – Expired"),
        ("Ana Jiménez",      "09:10 AM", "Yearly Premium",  "Entry", ft.Colors.GREEN,  ft.Colors.GREEN_100,  "Granted"),
        ("Carlos Ruiz",      "08:50 AM", "Monthly Basic",   "Exit",  ft.Colors.BLUE,   ft.Colors.BLUE_100,   "Exit OK"),
    ]
    activity_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Member")),
            ft.DataColumn(ft.Text("Time")),
            ft.DataColumn(ft.Text("Plan")),
            ft.DataColumn(ft.Text("Type")),
            ft.DataColumn(ft.Text("Result")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(r[0], weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Text(r[1])),
                ft.DataCell(ft.Text(r[2])),
                ft.DataCell(ft.Text(r[3])),
                ft.DataCell(ft.Chip(ft.Text(r[6]), bgcolor=r[5], label_text_style=ft.TextStyle(color=r[4]))),
            ])
            for r in activity_rows
        ],
        expand=True
    )

    # ── Revenue mini-chart (visual bars) ───────────────────────────────
    months = [("Ene","28k"),("Feb","32k"),("Mar","38k"),("Abr","45k")]
    max_h = 80
    bar_vals = [28, 32, 38, 45]
    bar_max = 45

    def bar_col(label, val, amount):
        h = int(max_h * val / bar_max)
        return ft.Column([
            ft.Text(amount, size=10, weight=ft.FontWeight.BOLD),
            ft.Container(bgcolor=ft.Colors.BLUE_400, width=28, height=h, border_radius=4),
            ft.Text(label, size=10, color=ft.Colors.ON_SURFACE_VARIANT),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4)

    revenue_chart = ft.Container(
        content=ft.Column([
            ft.Text("Revenue (Last 4 mo.)", size=14, weight=ft.FontWeight.BOLD),
            ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
            ft.Row([bar_col(m, v, a) for (m, a), v in zip(months, bar_vals)],
                   alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                   vertical_alignment=ft.CrossAxisAlignment.END),
        ]),
        bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=True
    )

    # ── Plan distribution mini ──────────────────────────────────────────
    plans_dist = ft.Container(
        content=ft.Column([
            ft.Text("Plan Distribution", size=14, weight=ft.FontWeight.BOLD),
            ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
            *[
                ft.Row([
                    ft.Text(lbl, expand=True, size=12),
                    ft.Container(bgcolor=clr, width=int(pct * 0.8), height=14, border_radius=6),
                    ft.Text(f"{pct}%", size=12, width=36, text_align=ft.TextAlign.RIGHT),
                ])
                for lbl, pct, clr in [
                    ("Monthly Basic",      45, ft.Colors.BLUE_400),
                    ("Quarterly Standard", 35, ft.Colors.PURPLE_400),
                    ("Yearly Premium",     20, ft.Colors.GREEN_400),
                ]
            ]
        ], spacing=10),
        bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=True
    )

    # ── Quick actions ───────────────────────────────────────────────────
    def quick_action(label, icon, color):
        return ft.ElevatedButton(
            label, icon=icon, bgcolor=color, color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            height=40
        )

    quick_actions = ft.Container(
        content=ft.Column([
            ft.Text("Quick Actions", size=14, weight=ft.FontWeight.BOLD),
            ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
            ft.Row([
                quick_action("New Member",   ft.Icons.PERSON_ADD,  ft.Colors.BLUE_700),
                quick_action("Record Payment", ft.Icons.ADD_CARD,   ft.Colors.GREEN_700),
                quick_action("Manual Log",     ft.Icons.LOGIN,       ft.Colors.ORANGE_700),
            ], wrap=True, spacing=8)
        ], spacing=0),
        bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=False
    )

    # ── Full layout ─────────────────────────────────────────────────────
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Sports Club – Live Overview", color=ft.Colors.ON_SURFACE_VARIANT, size=13),
                ], expand=True),
                ft.IconButton(ft.Icons.REFRESH)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            stats_row,

            ft.Row([revenue_chart, plans_dist], spacing=12, expand=False),

            quick_actions,

            ft.Text("Recent Access Activity", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([activity_table], scroll=ft.ScrollMode.AUTO, expand=True),
                bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=10, expand=True
            ),
        ], spacing=16, expand=True, scroll=ft.ScrollMode.AUTO),
        padding=28, expand=True
    )
