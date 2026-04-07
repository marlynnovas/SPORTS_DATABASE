from datetime import datetime, date, timedelta
from database.connection import get_connection

def create_membership(member_id, plan_id, duration_days):
    """Crea una nueva membresía calculando la fecha de fin basada en días."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        start_date = date.today()
        end_date = start_date + timedelta(days=duration_days)

        cursor.execute("""
            INSERT INTO memberships (member_id, plan_id, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (member_id, plan_id, start_date, end_date, "active"))

        conn.commit()
    except Exception as e:
        print(f"Error creating membership: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()


def get_active_membership(member_id):
    """Obtiene la membresía más reciente de un miembro."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM memberships
            WHERE member_id = ?
            ORDER BY end_date DESC
            LIMIT 1
        """, (member_id,))

        membership = cursor.fetchone()
        return dict(membership) if membership else None
    except Exception as e:
        print(f"Error fetching membership: {e}")
        return None
    finally:
        if conn: conn.close()


def update_membership_status(membership_id, status):
    """Actualiza manualmente el estado de una membresía."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE memberships
            SET status = ?
            WHERE id = ?
        """, (status, membership_id))

        conn.commit()
    except Exception as e:
        print(f"Error updating status: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()


def refresh_membership_status(membership):
    """
    Verifica si una membresía ha expirado y actualiza la DB si es necesario.
    Implementa la lógica proactiva requerida.
    """
    if not membership:
        return None

    try:
        # Convertir end_date si es string
        if isinstance(membership["end_date"], str):
            end_date = datetime.strptime(membership["end_date"], "%Y-%m-%d").date()
        else:
            end_date = membership["end_date"]

        if end_date < date.today() and membership["status"] == "active":
            update_membership_status(membership["id"], "expired")
            return "expired"

        return membership["status"]
    except Exception as e:
        print(f"Error refreshing status: {e}")
        return membership.get("status")


def auto_expire_memberships():
    """
    Busca todas las membresías activas cuya fecha de fin ya pasó y las marca como expiradas.
    Útil para procesos por lotes o al iniciar la app.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE memberships
            SET status = 'expired'
            WHERE status = 'active' AND end_date < ?
        """, (date.today(),))

        changed = cursor.rowcount
        conn.commit()
        return changed
    except Exception as e:
        print(f"Error in batch auto-expiration: {e}")
        if conn: conn.rollback()
        return 0
    finally:
        if conn: conn.close()