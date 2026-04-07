from datetime import datetime, timedelta
from database import get_connection

def create_membership(member_id, plan_id, duration_days):
    conn = get_connection()
    cursor = conn.cursor()

    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=duration_days)

    cursor.execute("""
        INSERT INTO memberships (member_id, plan_id, start_date, end_date, status)
        VALUES (?, ?, ?, ?, ?)
    """, (member_id, plan_id, start_date, end_date, "active"))

    conn.commit()
    conn.close()


def get_active_membership(member_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM memberships
        WHERE member_id = ?
        ORDER BY end_date DESC
        LIMIT 1
    """, (member_id,))

    membership = cursor.fetchone()
    conn.close()

    return membership


def update_membership_status(membership_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE memberships
        SET status = ?
        WHERE id = ?
    """, (status, membership_id))

    conn.commit()
    conn.close()


def refresh_membership_status(membership):
    """Actualiza estado automáticamente según fecha"""
    if not membership:
        return None

    from datetime import date

    end_date = datetime.strptime(membership["end_date"], "%Y-%m-%d").date()

    if end_date < date.today():
        return "expired"

    return membership["status"]