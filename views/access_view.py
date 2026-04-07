import flet as ft
from services.access_service import AccessService

def AccessLogView(page: ft.Page):
    # ── Stat cards ──────────────────────────────────────────────────────
    def mini_stat(title, val, clr):
        return ft.Container(
            content=ft.Column([
                ft.Text(val, size=24, weight=ft.FontWeight.BOLD, color=clr),
                ft.Text(title, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ], spacing=2),
            bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=10, padding=16, expand=True
        )

    stats_row = ft.Row([
        mini_stat("Total Today",    "24",  ft.Colors.BLUE),
        mini_stat("Granted",        "21",  ft.Colors.GREEN),
        mini_stat("Denied",         "3",   ft.Colors.RED),
        mini_stat("Peak Hour",      "9 AM",ft.Colors.ORANGE),
        mini_stat("Active Now",     "7",   ft.Colors.PURPLE),
    ], spacing=12)

    # ── Hourly activity bar ─────────────────────────────────────────────
    hourly = [
        ("6AM",1), ("7AM",3), ("8AM",5), ("9AM",9),
        ("10AM",7),("11AM",4),("12PM",3),("1PM",2),
    ]
    hr_max = max(v for _,v in hourly)

    def hr_bar(label, val):
        h = max(4, int(60 * val / hr_max))
        clr = ft.Colors.BLUE_600 if val == hr_max else ft.Colors.BLUE_300
        return ft.Column([
            ft.Text(str(val), size=10, weight=ft.FontWeight.BOLD),
            ft.Container(bgcolor=clr, width=22, height=h, border_radius=4),
            ft.Text(label, size=9, color=ft.Colors.ON_SURFACE_VARIANT),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3)

    traffic_chart = ft.Container(
        content=ft.Column([
            ft.Text("Hourly Traffic (Today)", size=14, weight=ft.FontWeight.BOLD),
            ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
            ft.Row(
                [hr_bar(l, v) for l, v in hourly],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.END
            )
        ]),
        bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=True
    )

    # ── Status pie-like (text bars) ─────────────────────────────────────
    status_summary = ft.Container(
        content=ft.Column([
            ft.Text("Access Outcomes (Week)", size=14, weight=ft.FontWeight.BOLD),
            ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
            *[
                ft.Row([
                    ft.Text(lbl, expand=True, size=12),
                    ft.Container(bgcolor=clr, width=int(pct * 0.9), height=14, border_radius=6),
                    ft.Text(f"{cnt}", size=12, width=36, text_align=ft.TextAlign.RIGHT),
                ])
                for lbl, cnt, pct, clr in [
                    ("Granted", 87, 87, ft.Colors.GREEN_400),
                    ("Denied",  13, 13, ft.Colors.RED_400),
                ]
            ]
        ], spacing=10),
        bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=True
    )

    # ── Log table ───────────────────────────────────────────────────────
    table = ft.DataTable(
        column_spacing=20,
        columns=[
            ft.DataColumn(ft.Text("Date & Time")),
            ft.DataColumn(ft.Text("Member")),
            ft.DataColumn(ft.Text("Result")),
            ft.DataColumn(ft.Text("Message")),
        ],
        rows=[],
        expand=True
    )

    def refresh_table(e=None):
        table.rows.clear()
        # Hardcoded entries + real DB entries
        hardcoded = [
            ("2024-04-07 10:43:00", "Juan Perez",       True,  "Valid membership"),
            ("2024-04-07 10:30:00", "Maria Rodriguez",  True,  "Valid membership"),
            ("2024-04-07 09:55:00", "Pedro García",     True,  "Valid membership"),
            ("2024-04-07 09:30:00", "Luis Martínez",    False, "Membership expired"),
            ("2024-04-07 09:10:00", "Ana Jiménez",      True,  "Valid membership"),
            ("2024-04-07 08:50:00", "Carlos Ruiz",      True,  "Valid membership"),
        ]

        logs = AccessService.get_recent_logs()
        # Combine hardcoded + real
        all_logs = [(h[0], h[1], "", h[2], h[3]) for h in hardcoded]
        for log in logs:
            all_logs.append((log["access_time"], log["first_name"], log["last_name"], bool(log["granted"]), log["message"] or "—"))

        for entry in all_logs:
            ts, name1, name2, granted, msg = entry
            full_name = f"{name1} {name2}".strip() if name2 else name1
            chip_c  = ft.Colors.GREEN if granted else ft.Colors.RED
            chip_bg = ft.Colors.GREEN_100 if granted else ft.Colors.RED_100
            label   = "Granted" if granted else "Denied"
            table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(ts)),
                ft.DataCell(ft.Text(full_name, weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Chip(ft.Text(label), bgcolor=chip_bg, label_text_style=ft.TextStyle(color=chip_c))),
                ft.DataCell(ft.Text(msg)),
            ]))
        page.update()

    refresh_table()

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Access Logs", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Real-time access monitoring and history", color=ft.Colors.ON_SURFACE_VARIANT, size=13),
                ], expand=True),
                ft.IconButton(ft.Icons.REFRESH, on_click=refresh_table)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            stats_row,
            ft.Row([traffic_chart, status_summary], spacing=12, expand=False),
            ft.Text("Access History", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([table], scroll=ft.ScrollMode.AUTO, expand=True),
                bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=10, expand=True
            )
        ], spacing=16, expand=True, scroll=ft.ScrollMode.AUTO),
        padding=28, expand=True
    )
