from datetime import datetime
from database import get_connection
from membership_service import update_membership_status

def register_payment(member_id, membership_id, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO payments (member_id, membership_id, amount, payment_status)
        VALUES (?, ?, ?, 'paid')
    """, (member_id, membership_id, amount))

    # 🔥 cuando paga → se activa
    update_membership_status(membership_id, "active")

    conn.commit()
    conn.close()