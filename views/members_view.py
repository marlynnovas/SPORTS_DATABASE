import flet as ft
from services.member_service import MemberService


def MembersView(page: ft.Page):

    # ── stat cards ───────────────────────────────────────────────────────
    def mini_stat(title, val, clr):
        return ft.Container(
            content=ft.Column([
                ft.Text(str(val), size=24, weight=ft.FontWeight.BOLD, color=clr),
                ft.Text(title, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ], spacing=2),
            bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=10, padding=16, expand=True
        )

    def make_stats():
        return ft.Row([
            mini_stat("Total Members",     MemberService.count_members(),             ft.Colors.BLUE),
            mini_stat("Active",            MemberService.count_by_status("active"),   ft.Colors.GREEN),
            mini_stat("Expired",           MemberService.count_by_status("expired"),  ft.Colors.RED),
            mini_stat("No Plan",           MemberService.count_no_plan(),             ft.Colors.GREY),
            mini_stat("Renewals this mo.", MemberService.count_renewals_this_month(), ft.Colors.ORANGE),
        ], spacing=12)

    stats_container = ft.Container(content=make_stats())

    # ── add member dialog ────────────────────────────────────────────────
    first_name_input = ft.TextField(label="First Name")
    last_name_input  = ft.TextField(label="Last Name")
    email_input      = ft.TextField(label="Email")
    phone_input      = ft.TextField(label="Phone")

    def save_member(e):
        if not first_name_input.value or not last_name_input.value or not email_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Fill required fields"), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()
            return
        MemberService.create_member(
            first_name_input.value, last_name_input.value,
            email_input.value, phone_input.value
        )
        # clear
        for f in [first_name_input, last_name_input, email_input, phone_input]:
            f.value = ""
        add_dialog.open = False
        refresh()
        page.update()

    add_dialog = ft.AlertDialog(
        title=ft.Text("Add New Member"),
        content=ft.Column([first_name_input, last_name_input, email_input, phone_input], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=lambda _: setattr(add_dialog, "open", False)),
            ft.ElevatedButton("Save", on_click=save_member),
        ]
    )
    page.overlay.append(add_dialog)

    # ── toolbar ──────────────────────────────────────────────────────────
    search_bar = ft.TextField(
        prefix_icon=ft.Icons.SEARCH,
        hint_text="Search members…",
        height=42, width=280, border_radius=8,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        border=ft.border.all(0, ft.Colors.TRANSPARENT), content_padding=10,
        on_change=lambda e: filter_table(e.control.value)
    )

    add_btn = ft.ElevatedButton(
        "Add Member", icon=ft.Icons.PERSON_ADD,
        bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE, height=42,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: setattr(add_dialog, "open", True)
    )

    # ── data table ───────────────────────────────────────────────────────
    table = ft.DataTable(
        column_spacing=20,
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Full Name")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Phone")),
            ft.DataColumn(ft.Text("Plan")),
            ft.DataColumn(ft.Text("Ends")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Actions")),
        ],
        rows=[],
        expand=True
    )

    all_members_cache = []

    def build_rows(members):
        rows = []
        STATUS_COLORS = {
            "active":   (ft.Colors.GREEN,  ft.Colors.GREEN_100),
            "expired":  (ft.Colors.RED,    ft.Colors.RED_100),
            "canceled": (ft.Colors.ORANGE, ft.Colors.ORANGE_100),
        }
        for m in members:
            status = m["membership_status"] or "none"
            clr, bg = STATUS_COLORS.get(status, (ft.Colors.GREY, ft.Colors.GREY_100))
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(m["id"]))),
                ft.DataCell(ft.Text(f"{m['first_name']} {m['last_name']}", weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Text(m["email"])),
                ft.DataCell(ft.Text(m["phone"] or "—")),
                ft.DataCell(ft.Text(m["plan_name"] or "No Plan")),
                ft.DataCell(ft.Text(m["end_date"] or "—")),
                ft.DataCell(ft.Chip(ft.Text(status.capitalize()), bgcolor=bg,
                                    label_text_style=ft.TextStyle(color=clr))),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.Icons.EDIT,   icon_color=ft.Colors.BLUE_400),
                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400),
                ])),
            ]))
        return rows

    def filter_table(query: str = ""):
        q = query.lower()
        filtered = [m for m in all_members_cache
                    if q in m["first_name"].lower() or q in m["last_name"].lower()
                    or q in m["email"].lower()]
        table.rows.clear()
        table.rows.extend(build_rows(filtered))
        page.update()

    def refresh(e=None):
        nonlocal all_members_cache
        all_members_cache = list(MemberService.get_all_members())
        table.rows.clear()
        table.rows.extend(build_rows(all_members_cache))
        # rebuild stats
        stats_container.content = make_stats()
        page.update()

    refresh()

    return ft.Container(
        content=ft.Column([
            ft.Text("Members", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Manage your club members and their memberships",
                    color=ft.Colors.ON_SURFACE_VARIANT, size=13),
            stats_container,
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Member List", size=18, weight=ft.FontWeight.BOLD, expand=True),
                        search_bar, add_btn,
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(height=6, color=ft.Colors.TRANSPARENT),
                    ft.Column([table], scroll=ft.ScrollMode.AUTO, expand=True),
                ], expand=True),
                bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=18, expand=True
            ),
        ], spacing=16, expand=True, scroll=ft.ScrollMode.AUTO),
        padding=28, expand=True
    )
