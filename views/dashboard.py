import flet as ft
from services.member_service import MemberService
from services.access_service import AccessService
from services.payment_service import PaymentService


def DashboardView(page: ft.Page):

    # ── helpers ─────────────────────────────────────────────────────────
    def stat_card(title, value, subtitle, icon, color):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, size=24, color=ft.Colors.WHITE),
                        bgcolor=color, border_radius=10, padding=10,
                        width=44, height=44
                    ),
                    ft.Column([
                        ft.Text(str(value), size=26, weight=ft.FontWeight.BOLD),
                        ft.Text(title, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                    ], spacing=0, expand=True),
                ], spacing=12),
                ft.Text(subtitle, size=11, color=ft.Colors.ON_SURFACE_VARIANT),
            ], spacing=6),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=12, padding=18, expand=True
        )

    # ── fetch stats ──────────────────────────────────────────────────────
    total_members  = MemberService.count_members()
    active_members = MemberService.count_by_status("active")
    revenue_mtd    = PaymentService.revenue_mtd()
    access_today   = AccessService.count_today()
    pending_bills  = PaymentService.count_by_status("pending")

    stats_row = ft.Row([
        stat_card("Total Members",  total_members,           "All registered",         ft.Icons.PEOPLE,        ft.Colors.BLUE_600),
        stat_card("Active Plans",   active_members,          "Current memberships",     ft.Icons.CHECK_CIRCLE,  ft.Colors.GREEN_600),
        stat_card("Revenue (MTD)",  f"${revenue_mtd:,.0f}",  "Completed payments",      ft.Icons.ATTACH_MONEY,  ft.Colors.PURPLE_600),
        stat_card("Access Today",   access_today,            "Entries logged today",    ft.Icons.LOGIN,         ft.Colors.ORANGE_600),
        stat_card("Pending Bills",  pending_bills,           "Awaiting payment",        ft.Icons.RECEIPT_LONG,  ft.Colors.RED_600),
    ], spacing=12)

    # ── monthly revenue bar chart ────────────────────────────────────────
    monthly = PaymentService.monthly_revenue(months=6)

    def bar_col(label, val, bar_max):
        h = max(4, int(80 * val / bar_max)) if bar_max else 4
        return ft.Column([
            ft.Text(f"${val/1000:.0f}k" if val >= 1000 else f"${val:.0f}", size=10, weight=ft.FontWeight.BOLD),
            ft.Container(bgcolor=ft.Colors.BLUE_400, width=28, height=h, border_radius=4),
            ft.Text(label[-5:], size=9, color=ft.Colors.ON_SURFACE_VARIANT),  # show YYYY-MM
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4)

    bar_max = max((v for _, v in monthly), default=1)
    revenue_chart = ft.Container(
        content=ft.Column([
            ft.Text("Monthly Revenue", size=14, weight=ft.FontWeight.BOLD),
            ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
            ft.Row(
                [bar_col(l, v, bar_max) for l, v in monthly] if monthly
                else [ft.Text("No payment data yet", color=ft.Colors.ON_SURFACE_VARIANT, size=12)],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.END
            ),
        ]),
        bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=True
    )

    # ── membership status distribution ──────────────────────────────────
    exp_count = MemberService.count_by_status("expired")
    total_ms  = active_members + exp_count or 1
    act_pct   = int(active_members * 100 / total_ms)
    exp_pct   = 100 - act_pct

    dist_chart = ft.Container(
        content=ft.Column([
            ft.Text("Membership Status", size=14, weight=ft.FontWeight.BOLD),
            ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
            *[
                ft.Row([
                    ft.Text(lbl, expand=True, size=12),
                    ft.Container(bgcolor=clr, width=int(pct * 0.9), height=14, border_radius=6),
                    ft.Text(f"{pct}%", size=12, width=40, text_align=ft.TextAlign.RIGHT),
                ])
                for lbl, pct, clr in [
                    ("Active",  act_pct, ft.Colors.GREEN_400),
                    ("Expired", exp_pct, ft.Colors.RED_400),
                ]
            ]
        ], spacing=10),
        bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=True
    )

    # ── quick actions ────────────────────────────────────────────────────
    quick_actions = ft.Container(
        content=ft.Column([
            ft.Text("Quick Actions", size=14, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton("New Member",     icon=ft.Icons.PERSON_ADD,  bgcolor=ft.Colors.BLUE_700,  color=ft.Colors.WHITE,
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), height=38),
                ft.ElevatedButton("Record Payment", icon=ft.Icons.ADD_CARD,    bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE,
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), height=38),
                ft.ElevatedButton("Manual Log",     icon=ft.Icons.LOGIN,       bgcolor=ft.Colors.ORANGE_700,color=ft.Colors.WHITE,
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), height=38),
            ], spacing=10, wrap=True),
        ], spacing=10),
        bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18
    )

    # ── recent access activity ───────────────────────────────────────────
    logs = AccessService.get_recent_logs(limit=8)

    def log_row(log):
        granted = bool(log["granted"])
        chip_c  = ft.Colors.GREEN if granted else ft.Colors.RED
        chip_bg = ft.Colors.GREEN_100 if granted else ft.Colors.RED_100
        label   = "Granted" if granted else "Denied"
        name    = f"{log['first_name']} {log['last_name']}"
        ts      = log["access_time"]
        return ft.DataRow(cells=[
            ft.DataCell(ft.Text(name,  weight=ft.FontWeight.W_500)),
            ft.DataCell(ft.Text(ts)),
            ft.DataCell(ft.Chip(ft.Text(label), bgcolor=chip_bg, label_text_style=ft.TextStyle(color=chip_c))),
            ft.DataCell(ft.Text(log["message"] or "—")),
        ])

    activity_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Member")),
            ft.DataColumn(ft.Text("Time")),
            ft.DataColumn(ft.Text("Result")),
            ft.DataColumn(ft.Text("Message")),
        ],
        rows=[log_row(l) for l in logs] if logs
             else [ft.DataRow(cells=[ft.DataCell(ft.Text("No access records yet", color=ft.Colors.ON_SURFACE_VARIANT))] + [ft.DataCell(ft.Text("")) for _ in range(3)])],
        expand=True
    )

    # ── layout ───────────────────────────────────────────────────────────
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
            ft.Row([revenue_chart, dist_chart], spacing=12),
            quick_actions,
            ft.Text("Recent Access Activity", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([activity_table], scroll=ft.ScrollMode.AUTO, expand=True),
                bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=10, expand=True
            ),
        ], spacing=16, expand=True, scroll=ft.ScrollMode.AUTO),
        padding=28, expand=True
    )
