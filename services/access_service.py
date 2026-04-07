from datetime import datetime
from database import get_connection
from membership_service import get_active_membership, refresh_membership_status

def validate_access(member_id):
    conn = get_connection()
    cursor = conn.cursor()

    membership = get_active_membership(member_id)

    if not membership:
        result = "denied"
        message = "No membership found"

    else:
        status = refresh_membership_status(membership)

        if status != "active":
            result = "denied"
            message = f"Membership {status}"
        else:
            result = "granted"
            message = "Access granted"

    # 🔥 registrar intento SIEMPRE
    cursor.execute("""
        INSERT INTO access_logs (member_id, result, message)
        VALUES (?, ?, ?)
    """, (member_id, result, message))

    conn.commit()
    conn.close()

    return {
        "result": result,
        "message": message
    }