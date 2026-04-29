import flet as ft
from services.payment_service import PaymentService
from services.membership_service import MembershipService
from datetime import datetime

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

    # ── Record Payment Dialog ───────────────────────────────────────────
    membership_dropdown = ft.Dropdown(label="Select Membership", options=[])
    amount_input = ft.TextField(label="Amount ($)", keyboard_type=ft.KeyboardType.NUMBER)
    status_dropdown = ft.Dropdown(
        label="Status",
        value="completed",
        options=[
            ft.dropdown.Option("completed", "Completed"),
            ft.dropdown.Option("pending", "Pending"),
            ft.dropdown.Option("failed", "Failed"),
        ]
    )

    def load_memberships():
        ms_list = MembershipService.get_all_memberships()
        membership_dropdown.options = [
            ft.dropdown.Option(key=str(m["id"]), text=f"#{m['id']} - {m['first_name']} {m['last_name']} ({m['plan_name']})")
            for m in ms_list
        ]
        page.update()

    def save_payment(e):
        if not membership_dropdown.value or not amount_input.value:
            return
        
        try:
            amt = float(amount_input.value)
            mid = int(membership_dropdown.value)
            PaymentService.create_payment(mid, amt, status_dropdown.value)
            pay_dialog.open = False
            refresh()
            page.update()
        except: pass

    pay_dialog = ft.AlertDialog(
        title=ft.Text("Record New Payment"),
        content=ft.Column([membership_dropdown, amount_input, status_dropdown], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=lambda _: setattr(pay_dialog, "open", False)),
            ft.ElevatedButton("Save Payment", on_click=save_payment),
        ]
    )
    page.overlay.append(pay_dialog)

    # ── Table ─────────────────────────────────────────────────────────
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Member")),
            ft.DataColumn(ft.Text("Amount")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Actions")),
        ],
        rows=[],
        expand=True
    )

    def refresh(e=None):
        stats_container.content = make_stats()
        table.rows.clear()
        payments = PaymentService.get_all_payments()
        for p in payments:
            def delete_cb(_, pid=p["id"]):
                PaymentService.delete_payment(pid)
                refresh()
                page.update()

            # Late payment warning logic
            is_pending  = p["status"] == "pending"
            is_overdue  = p["status"] == "failed"
            status_chip = ft.Chip(ft.Text(p["status"].capitalize()),
                                  bgcolor=ft.Colors.GREEN_100  if p["status"] == "completed"
                                     else ft.Colors.ORANGE_100 if is_pending
                                     else ft.Colors.RED_100)

            warning_icon = None
            if is_overdue:
                warning_icon = ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.RED_400, size=20, tooltip="⚠️ Payment failed – needs attention!")
            elif is_pending:
                warning_icon = ft.Icon(ft.Icons.SCHEDULE, color=ft.Colors.ORANGE_400, size=20, tooltip="⏳ Payment pending – remind member")

            name_cell_controls = [ft.Text(f"{p['first_name']} {p['last_name']}")]
            if warning_icon:
                name_cell_controls.append(warning_icon)

            table.rows.append(ft.DataRow(
                color=ft.Colors.RED_900 if is_overdue else (ft.Colors.ORANGE_900 if is_pending else None),
                cells=[
                    ft.DataCell(ft.Text(str(p["id"]))),
                    ft.DataCell(ft.Text(p["payment_date"])),
                    ft.DataCell(ft.Row(name_cell_controls, spacing=6)),
                    ft.DataCell(ft.Text(f"${p['amount']:,.2f}", weight=ft.FontWeight.BOLD)),
                    ft.DataCell(status_chip),
                    ft.DataCell(ft.Row([
                        ft.PopupMenuButton(
                            icon=ft.Icons.EDIT,
                            items=[
                                ft.PopupMenuItem(content=ft.Text("Mark Completed"), on_click=lambda _, pid=p["id"]: (PaymentService.update_payment_status(pid, "completed"), refresh(), page.update())),
                                ft.PopupMenuItem(content=ft.Text("Mark Pending"), on_click=lambda _, pid=p["id"]: (PaymentService.update_payment_status(pid, "pending"), refresh(), page.update())),
                                ft.PopupMenuItem(content=ft.Text("Mark Failed"), on_click=lambda _, pid=p["id"]: (PaymentService.update_payment_status(pid, "failed"), refresh(), page.update())),
                            ],
                            tooltip="Change Status"
                        ),
                        ft.IconButton(ft.Icons.RECEIPT, icon_color=ft.Colors.BLUE_400),
                        ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=delete_cb),
                    ])),
                ]))
        page.update()

    refresh()

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Payments & Billing", size=32, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Record Payment", icon=ft.Icons.ADD, on_click=lambda _: (load_memberships(), setattr(pay_dialog, "open", True)), bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            stats_container,
            ft.Container(
                content=ft.Column([table], scroll=ft.ScrollMode.AUTO, expand=True),
                bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=10, expand=True
            ),
        ], spacing=16, expand=True),
        padding=28, expand=True
    )
