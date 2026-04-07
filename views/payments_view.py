import flet as ft
from services.payment_service import PaymentService


def PaymentsView(page: ft.Page):

    # ── stat cards ───────────────────────────────────────────────────────
    def stat_card(title, val, sub, clr):
        return ft.Container(
            content=ft.Column([
                ft.Text(str(val), size=26, weight=ft.FontWeight.BOLD, color=clr),
                ft.Text(title, size=12, weight=ft.FontWeight.BOLD),
                ft.Text(sub,   size=11, color=ft.Colors.ON_SURFACE_VARIANT),
            ], spacing=2),
            bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=16, expand=True
        )

    def make_stats():
        rev     = PaymentService.revenue_mtd()
        pending = PaymentService.count_by_status("pending")
        overdue = PaymentService.count_by_status("failed")
        avg     = PaymentService.average_amount()
        count   = PaymentService.count_this_month()
        return ft.Row([
            stat_card("Revenue (MTD)",  f"${rev:,.0f}",  "Completed only",   ft.Colors.GREEN),
            stat_card("Pending",        pending,          "Awaiting payment",  ft.Colors.ORANGE),
            stat_card("Failed",         overdue,          "Needs attention",   ft.Colors.RED),
            stat_card("Avg Ticket",     f"${avg:,.0f}",  "Per transaction",   ft.Colors.BLUE),
            stat_card("Transactions",   count,            "This month",        ft.Colors.PURPLE),
        ], spacing=12)

    stats_container = ft.Container(content=make_stats())

    # ── revenue bar chart ────────────────────────────────────────────────
    def make_chart():
        monthly = PaymentService.monthly_revenue(months=6)
        if not monthly:
            return ft.Container(
                content=ft.Column([
                    ft.Text("Monthly Revenue", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text("No payment data yet", color=ft.Colors.ON_SURFACE_VARIANT, size=12),
                ]),
                bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=True
            )
        bar_max = max(v for _, v in monthly) or 1

        def bar(label, val):
            h = max(4, int(80 * val / bar_max))
            return ft.Column([
                ft.Text(f"${val/1000:.1f}k" if val >= 1000 else f"${val:.0f}", size=10, weight=ft.FontWeight.BOLD),
                ft.Container(bgcolor=ft.Colors.GREEN_400, width=28, height=h, border_radius=5),
                ft.Text(label[-5:], size=9, color=ft.Colors.ON_SURFACE_VARIANT),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4)

        return ft.Container(
            content=ft.Column([
                ft.Text("Monthly Revenue", size=14, weight=ft.FontWeight.BOLD),
                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                ft.Row([bar(l, v) for l, v in monthly],
                       alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                       vertical_alignment=ft.CrossAxisAlignment.END, spacing=12),
            ]),
            bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=True
        )

    chart_container = ft.Container(content=make_chart(), expand=True)

    # ── payment status distribution ──────────────────────────────────────
    def make_dist():
        completed = PaymentService.count_by_status("completed")
        pending   = PaymentService.count_by_status("pending")
        failed    = PaymentService.count_by_status("failed")
        total     = completed + pending + failed or 1

        def pct(n): return int(n * 100 / total)

        return ft.Container(
            content=ft.Column([
                ft.Text("Payment Status", size=14, weight=ft.FontWeight.BOLD),
                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                *[
                    ft.Row([
                        ft.Text(lbl, expand=True, size=12),
                        ft.Container(bgcolor=clr, width=max(4, int(pct(cnt) * 0.9)), height=14, border_radius=6),
                        ft.Text(f"{pct(cnt)}%", size=12, width=40, text_align=ft.TextAlign.RIGHT),
                    ])
                    for lbl, cnt, clr in [
                        ("Completed", completed, ft.Colors.GREEN_400),
                        ("Pending",   pending,   ft.Colors.ORANGE_400),
                        ("Failed",    failed,    ft.Colors.RED_400),
                    ]
                ]
            ], spacing=10),
            bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=True
        )

    dist_container = ft.Container(content=make_dist(), expand=True)

    # ── transactions table ───────────────────────────────────────────────
    STATUS_COLORS = {
        "completed": (ft.Colors.GREEN,  ft.Colors.GREEN_100),
        "pending":   (ft.Colors.ORANGE, ft.Colors.ORANGE_100),
        "failed":    (ft.Colors.RED,    ft.Colors.RED_100),
    }

    table = ft.DataTable(
        column_spacing=20,
        columns=[
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Member")),
            ft.DataColumn(ft.Text("Plan")),
            ft.DataColumn(ft.Text("Amount")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Actions")),
        ],
        rows=[],
        expand=True
    )

    def refresh(e=None):
        # stats
        stats_container.content = make_stats()
        chart_container.content = make_chart()
        dist_container.content  = make_dist()

        # table
        table.rows.clear()
        payments = PaymentService.get_all_payments()
        if payments:
            for p in payments:
                clr, bg = STATUS_COLORS.get(p["status"], (ft.Colors.GREY, ft.Colors.GREY_100))
                table.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(p["payment_date"])),
                    ft.DataCell(ft.Text(f"{p['first_name']} {p['last_name']}", weight=ft.FontWeight.W_500)),
                    ft.DataCell(ft.Text(p["plan_name"])),
                    ft.DataCell(ft.Text(f"${p['amount']:,.2f}", weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Chip(ft.Text(p["status"].capitalize()), bgcolor=bg,
                                        label_text_style=ft.TextStyle(color=clr))),
                    ft.DataCell(ft.IconButton(ft.Icons.RECEIPT, icon_color=ft.Colors.BLUE_400)),
                ]))
        else:
            table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text("No payment records yet", color=ft.Colors.ON_SURFACE_VARIANT)),
                *[ft.DataCell(ft.Text("")) for _ in range(5)],
            ]))
        page.update()

    refresh()

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Payments & Billing", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Track income, transactions and pending bills",
                            color=ft.Colors.ON_SURFACE_VARIANT, size=13),
                ], expand=True),
                ft.ElevatedButton("Record Payment", icon=ft.Icons.ADD_CARD,
                                  bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
                ft.IconButton(ft.Icons.REFRESH, on_click=refresh),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            stats_container,
            ft.Row([chart_container, dist_container], spacing=12),
            ft.Text("Transaction History", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([table], scroll=ft.ScrollMode.AUTO, expand=True),
                bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=10, expand=True
            ),
        ], spacing=16, expand=True, scroll=ft.ScrollMode.AUTO),
        padding=28, expand=True
    )
