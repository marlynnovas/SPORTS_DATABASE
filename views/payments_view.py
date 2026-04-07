import flet as ft

def PaymentsView(page: ft.Page):
    # ── Stat cards ──────────────────────────────────────────────────────
    def stat_card(title, val, sub, clr):
        return ft.Container(
            content=ft.Column([
                ft.Text(val, size=26, weight=ft.FontWeight.BOLD, color=clr),
                ft.Text(title, size=12, weight=ft.FontWeight.BOLD),
                ft.Text(sub, size=11, color=ft.Colors.ON_SURFACE_VARIANT),
            ], spacing=2),
            bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=16, expand=True
        )

    stats = ft.Row([
        stat_card("Revenue (MTD)",   "$45,200", "↑ 12% vs March",         ft.Colors.GREEN),
        stat_card("Pending",         "5",        "3 due this week",         ft.Colors.ORANGE),
        stat_card("Overdue",         "2",        "Action required",          ft.Colors.RED),
        stat_card("Avg Ticket",      "$5,150",   "Per transaction",          ft.Colors.BLUE),
        stat_card("Transactions",    "28",       "This month",               ft.Colors.PURPLE),
    ], spacing=12)

    # ── Monthly bars ────────────────────────────────────────────────────
    bar_data = [
        ("Ene", 28), ("Feb", 32), ("Mar", 38), ("Abr", 45),
    ]
    max_h = 90
    bar_max = max(v for _, v in bar_data)

    def bar(label, val):
        h = int(max_h * val / bar_max)
        return ft.Column([
            ft.Text(f"${val}k", size=10, weight=ft.FontWeight.BOLD),
            ft.Container(bgcolor=ft.Colors.GREEN_400, width=32, height=h, border_radius=5),
            ft.Text(label, size=10, color=ft.Colors.ON_SURFACE_VARIANT),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4)

    mini_chart = ft.Container(
        content=ft.Column([
            ft.Text("Monthly Revenue", size=14, weight=ft.FontWeight.BOLD),
            ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
            ft.Row([bar(l, v) for l, v in bar_data],
                   alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                   vertical_alignment=ft.CrossAxisAlignment.END, spacing=12)
        ]),
        bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=True
    )

    # ── Method distribution ─────────────────────────────────────────────
    methods = ft.Container(
        content=ft.Column([
            ft.Text("Payment Methods", size=14, weight=ft.FontWeight.BOLD),
            ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
            *[
                ft.Row([
                    ft.Text(lbl, expand=True, size=12),
                    ft.Container(bgcolor=clr, width=int(pct * 0.9), height=14, border_radius=6),
                    ft.Text(f"{pct}%", size=12, width=36, text_align=ft.TextAlign.RIGHT),
                ])
                for lbl, pct, clr in [
                    ("Cash",     40, ft.Colors.BLUE_400),
                    ("Card",     35, ft.Colors.GREEN_400),
                    ("Transfer", 25, ft.Colors.PURPLE_400),
                ]
            ]
        ], spacing=10),
        bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=True
    )

    # ── Transactions table ──────────────────────────────────────────────
    txs = [
        ("2024-04-07", "Juan Perez",      "Monthly Basic",      "$1,500",  "Cash",     "Paid",    ft.Colors.GREEN, ft.Colors.GREEN_100),
        ("2024-04-05", "Maria Rodriguez", "Yearly Premium",     "$15,000", "Card",     "Paid",    ft.Colors.GREEN, ft.Colors.GREEN_100),
        ("2024-04-05", "Pedro García",    "Quarterly Standard", "$4,000",  "Transfer", "Pending", ft.Colors.ORANGE, ft.Colors.ORANGE_100),
        ("2024-04-03", "Ana Jiménez",     "Monthly Basic",      "$1,500",  "Cash",     "Paid",    ft.Colors.GREEN, ft.Colors.GREEN_100),
        ("2024-04-01", "Carlos Ruiz",     "Yearly Premium",     "$15,000", "Card",     "Paid",    ft.Colors.GREEN, ft.Colors.GREEN_100),
        ("2024-03-28", "Luis Martínez",   "Monthly Basic",      "$1,500",  "Cash",     "Overdue", ft.Colors.RED, ft.Colors.RED_100),
        ("2024-03-25", "Juana Mora",      "Quarterly Standard", "$4,000",  "Transfer", "Paid",    ft.Colors.GREEN, ft.Colors.GREEN_100),
    ]

    table = ft.DataTable(
        column_spacing=20,
        columns=[
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Member")),
            ft.DataColumn(ft.Text("Plan")),
            ft.DataColumn(ft.Text("Amount")),
            ft.DataColumn(ft.Text("Method")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Actions")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(t[0])),
                ft.DataCell(ft.Text(t[1], weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Text(t[2])),
                ft.DataCell(ft.Text(t[3], weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(t[4])),
                ft.DataCell(ft.Chip(ft.Text(t[5]), bgcolor=t[7], label_text_style=ft.TextStyle(color=t[6]))),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.Icons.RECEIPT, icon_color=ft.Colors.BLUE_400),
                ])),
            ])
            for t in txs
        ],
        expand=True
    )

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Payments & Billing", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Track income, transactions and pending bills", color=ft.Colors.ON_SURFACE_VARIANT, size=13),
                ], expand=True),
                ft.ElevatedButton("Record Payment", icon=ft.Icons.ADD_CARD,
                                  bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            stats,
            ft.Row([mini_chart, methods], spacing=12, expand=False),
            ft.Text("Transaction History", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([table], scroll=ft.ScrollMode.AUTO, expand=True),
                bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=10, expand=True
            )
        ], spacing=16, expand=True, scroll=ft.ScrollMode.AUTO),
        padding=28, expand=True
    )
