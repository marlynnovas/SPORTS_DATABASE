import flet as ft
import csv
import io
from database.connection import get_connection
from services.member_service import MemberService
from services.payment_service import PaymentService
from services.access_service import AccessService

def ReportsView(page: ft.Page):
    
    # ── Export Logic ──────────────────────────────────────────────────
    def export_csv(e):
        from datetime import datetime
        import platform
        import subprocess
        import os
        
        default_filename = f"members_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        save_path = None
        
        sys_plat = platform.system()
        if sys_plat == "Linux":
            try:
                res = subprocess.run(
                    ['zenity', '--file-selection', '--save', '--confirm-overwrite', 
                     '--title', 'Save Report', '--filename', default_filename, '--file-filter=*.csv'], 
                    capture_output=True, text=True
                )
                if res.returncode == 0:
                    save_path = res.stdout.strip()
            except Exception:
                pass
        elif sys_plat == "Darwin":
            try:
                res = subprocess.run([
                    'osascript', '-e',
                    f'set theFile to choose file name with prompt "Save Report As:" default name "{default_filename}"',
                    '-e', 'POSIX path of theFile'
                ], capture_output=True, text=True)
                if res.returncode == 0:
                    save_path = res.stdout.strip()
            except Exception:
                pass
        else:
            try:
                import tkinter as tk
                from tkinter import filedialog
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                path = filedialog.asksaveasfilename(
                    defaultextension=".csv", 
                    initialfile=default_filename, 
                    title="Save Report",
                    filetypes=[("CSV files", "*.csv")]
                )
                root.destroy()
                if path:
                    save_path = path
            except Exception:
                pass
                
        # Fallback if no path chosen or user cancelled
        if not save_path:
            return
            
        # Export logic
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM active_members_view")
        rows = cursor.fetchall()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([d[0] for d in cursor.description])
        writer.writerows(rows)
        conn.close()
        
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(output.getvalue())
            
        page.snack_bar = ft.SnackBar(ft.Text(f"Report exported to {save_path}"), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        page.update()
        
        # Open directory
        folder = os.path.dirname(save_path)
        if platform.system() == "Windows":
            os.startfile(folder)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", folder])
        else:
            subprocess.Popen(["xdg-open", folder])

    def print_report(e):
        import os
        import subprocess
        import platform
        import tempfile
        from datetime import datetime

        # ── Fetch data ──────────────────────────────────────────────
        total   = MemberService.count_members()
        active  = MemberService.count_by_status("active")
        revenue = PaymentService.revenue_mtd()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM denied_access_summary")
        denied_rows = cursor.fetchall()
        cursor.execute("SELECT * FROM active_members_view")
        members_rows = cursor.fetchall()
        members_cols = [d[0] for d in cursor.description]
        conn.close()

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        # ── Build denied-access rows ─────────────────────────────────
        denied_html = "".join(
            f"<tr><td>{r[0]}</td><td style='color:#e53935;text-align:center'>{r[1]}</td><td>{r[2]}</td></tr>"
            for r in denied_rows
        ) or "<tr><td colspan='3' style='text-align:center;color:#888'>No denied access records</td></tr>"

        # ── Build members rows ───────────────────────────────────────
        members_header = "".join(f"<th>{c}</th>" for c in members_cols)
        members_body   = "".join(
            "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
            for row in members_rows
        ) or f"<tr><td colspan='{len(members_cols)}' style='text-align:center;color:#888'>No data</td></tr>"

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Sports Club – System Report</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Inter', sans-serif; background: #f5f5f5; color: #212121; padding: 32px; }}
  h1 {{ font-size: 26px; font-weight: 700; margin-bottom: 4px; }}
  .subtitle {{ color: #757575; font-size: 13px; margin-bottom: 28px; }}
  .stats {{ display: flex; gap: 16px; margin-bottom: 32px; }}
  .card {{ flex: 1; background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,.1); }}
  .card .value {{ font-size: 28px; font-weight: 700; }}
  .card .label {{ font-size: 13px; color: #757575; margin-top: 4px; }}
  .green {{ color: #43a047; }}
  .purple {{ color: #7b1fa2; }}
  section {{ background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,.1); margin-bottom: 24px; }}
  section h2 {{ font-size: 16px; font-weight: 600; margin-bottom: 14px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ text-align: left; padding: 8px 12px; background: #f0f0f0; font-weight: 600; }}
  td {{ padding: 7px 12px; border-bottom: 1px solid #f0f0f0; }}
  tr:last-child td {{ border-bottom: none; }}
  .footer {{ text-align: center; font-size: 11px; color: #9e9e9e; margin-top: 24px; }}
  @media print {{
    body {{ background: #fff; padding: 0; }}
    .card, section {{ box-shadow: none; border: 1px solid #ddd; }}
  }}
</style>
</head>
<body>
<h1>Sports Club – System Report</h1>
<p class="subtitle">Generated on {now_str}</p>

<div class="stats">
  <div class="card">
    <div class="value">{total}</div>
    <div class="label">Total Members</div>
  </div>
  <div class="card">
    <div class="value green">{active}</div>
    <div class="label">Active Accounts</div>
  </div>
  <div class="card">
    <div class="value purple">${revenue:,.0f}</div>
    <div class="label">Revenue MTD</div>
  </div>
</div>

<section>
  <h2>Active Members</h2>
  <table>
    <thead><tr>{members_header}</tr></thead>
    <tbody>{members_body}</tbody>
  </table>
</section>

<section>
  <h2>Access Issues Summary</h2>
  <table>
    <thead><tr><th>Member</th><th>Denied Count</th><th>Last Attempt</th></tr></thead>
    <tbody>{denied_html}</tbody>
  </table>
</section>

<p class="footer">Sports Club Management System &nbsp;|&nbsp; Printed on {now_str}</p>
<script>window.onload = function() {{ window.print(); }}</script>
</body>
</html>"""

        # ── Write to temp file and open in browser ───────────────────
        tmp = tempfile.NamedTemporaryFile(
            delete=False, suffix=".html",
            prefix="sports_club_report_", mode="w", encoding="utf-8"
        )
        tmp.write(html)
        tmp.close()

        plat = platform.system()
        if plat == "Windows":
            os.startfile(tmp.name)
        elif plat == "Darwin":
            subprocess.Popen(["open", tmp.name])
        else:
            subprocess.Popen(["xdg-open", tmp.name])

        page.snack_bar = ft.SnackBar(
            ft.Text("Print preview opened in browser – press Ctrl+P to print"),
            bgcolor=ft.Colors.BLUE
        )
        page.snack_bar.open = True
        page.update()

    # ── Export Payments CSV ───────────────────────────────────────────────
    def export_payments_csv(e):
        from datetime import datetime
        import platform, subprocess, os
        default_filename = f"payments_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        save_path = None
        if platform.system() == "Linux":
            try:
                res = subprocess.run(
                    ['zenity', '--file-selection', '--save', '--confirm-overwrite',
                     '--title', 'Save Payments Report', '--filename', default_filename, '--file-filter=*.csv'],
                    capture_output=True, text=True)
                if res.returncode == 0:
                    save_path = res.stdout.strip()
            except Exception:
                pass
        elif platform.system() == "Darwin":
            try:
                res = subprocess.run(['osascript', '-e', f'set theFile to choose file name with prompt "Save Report As:" default name "{default_filename}"', '-e', 'POSIX path of theFile'], capture_output=True, text=True)
                if res.returncode == 0: save_path = res.stdout.strip()
            except Exception: pass
        else:
            try:
                import tkinter as tk
                from tkinter import filedialog
                root = tk.Tk(); root.withdraw(); root.attributes('-topmost', True)
                path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=default_filename,
                    title="Save Payments Report", filetypes=[("CSV files", "*.csv")])
                root.destroy()
                if path: save_path = path
            except Exception:
                pass
        if not save_path:
            return
        payments = PaymentService.get_all_payments(limit=10000)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Member First", "Member Last", "Plan", "Amount", "Date", "Status"])
        for p in payments:
            writer.writerow([p["id"], p["first_name"], p["last_name"], p["plan_name"], p["amount"], p["payment_date"], p["status"]])
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(output.getvalue())
        page.snack_bar = ft.SnackBar(ft.Text(f"Payments exported to {save_path}"), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        page.update()
        folder = os.path.dirname(save_path)
        if platform.system() == "Windows": os.startfile(folder)
        elif platform.system() == "Darwin": subprocess.Popen(["open", folder])
        else: subprocess.Popen(["xdg-open", folder])

    # ── Export Attendance CSV ─────────────────────────────────────────────
    def export_access_csv(e):
        from datetime import datetime
        import platform, subprocess, os
        default_filename = f"attendance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        save_path = None
        if platform.system() == "Linux":
            try:
                res = subprocess.run(
                    ['zenity', '--file-selection', '--save', '--confirm-overwrite',
                     '--title', 'Save Attendance Report', '--filename', default_filename, '--file-filter=*.csv'],
                    capture_output=True, text=True)
                if res.returncode == 0:
                    save_path = res.stdout.strip()
            except Exception:
                pass
        elif platform.system() == "Darwin":
            try:
                res = subprocess.run(['osascript', '-e', f'set theFile to choose file name with prompt "Save Report As:" default name "{default_filename}"', '-e', 'POSIX path of theFile'], capture_output=True, text=True)
                if res.returncode == 0: save_path = res.stdout.strip()
            except Exception: pass
        else:
            try:
                import tkinter as tk
                from tkinter import filedialog
                root = tk.Tk(); root.withdraw(); root.attributes('-topmost', True)
                path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=default_filename,
                    title="Save Attendance Report", filetypes=[("CSV files", "*.csv")])
                root.destroy()
                if path: save_path = path
            except Exception:
                pass
        if not save_path:
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT al.id, m.first_name, m.last_name, al.access_time,
                   CASE WHEN al.granted THEN 'Granted' ELSE 'Denied' END as result, al.message
            FROM access_logs al
            JOIN members m ON al.member_id = m.id
            ORDER BY al.access_time DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Log ID", "First Name", "Last Name", "Access Time", "Result", "Message"])
        for r in rows:
            writer.writerow([r[0], r[1], r[2], r[3], r[4], r[5]])
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(output.getvalue())
        page.snack_bar = ft.SnackBar(ft.Text(f"Attendance exported to {save_path}"), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        page.update()
        folder = os.path.dirname(save_path)
        if platform.system() == "Windows": os.startfile(folder)
        elif platform.system() == "Darwin": subprocess.Popen(["open", folder])
        else: subprocess.Popen(["xdg-open", folder])

    # ── Summary Content ───────────────────────────────────────────────
    def make_stats_row():
        total, active, revenue = MemberService.count_members(), MemberService.count_by_status("active"), PaymentService.revenue_mtd()
        return ft.Row([
            ft.Container(ft.Column([ft.Text(str(total), size=24, weight=ft.FontWeight.BOLD), ft.Text("Total Members")]), width=200, bgcolor=ft.Colors.SURFACE_CONTAINER, padding=20, border_radius=12),
            ft.Container(ft.Column([ft.Text(str(active), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN), ft.Text("Active Accounts")]), width=200, bgcolor=ft.Colors.SURFACE_CONTAINER, padding=20, border_radius=12),
            ft.Container(ft.Column([ft.Text(f"${revenue:,.0f}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE), ft.Text("Revenue MTD")]), width=200, bgcolor=ft.Colors.SURFACE_CONTAINER, padding=20, border_radius=12),
        ], spacing=12, wrap=True)

    # Table for Denied Access
    def get_denied_table():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM denied_access_summary")
        rows = cursor.fetchall()
        conn.close()
        return ft.DataTable(
            columns=[ft.DataColumn(ft.Text("Member")), ft.DataColumn(ft.Text("Denied Access Count")), ft.DataColumn(ft.Text("Last Attempt"))],
            rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(r[0])), ft.DataCell(ft.Text(str(r[1]), color=ft.Colors.RED)), ft.DataCell(ft.Text(r[2]))]) for r in rows],
            expand=True
        )

    from datetime import datetime
    
    return ft.Container(
        content=ft.Column([
            ft.Column([
                ft.Text("System Reports", size=32, weight=ft.FontWeight.BOLD),
                ft.Text(f"Reports generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Container(height=10),
                ft.Row([
                    ft.ElevatedButton("Export Members", icon=ft.Icons.PEOPLE, on_click=export_csv),
                    ft.ElevatedButton("Export Payments", icon=ft.Icons.PAYMENTS, on_click=export_payments_csv),
                    ft.ElevatedButton("Export Attendance", icon=ft.Icons.HISTORY, on_click=export_access_csv),
                    ft.ElevatedButton("Print Report", icon=ft.Icons.PRINT, on_click=print_report),
                ], spacing=8, wrap=True)
            ]),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            make_stats_row(),
            ft.Text("Access Issues Summary", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([get_denied_table()], scroll=ft.ScrollMode.AUTO, expand=True),
                bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=12, padding=15, expand=True
            ),
        ], spacing=16, expand=True, scroll=ft.ScrollMode.AUTO),
        padding=28, expand=True
    )
