from database.connection import get_connection
from services.membership_service import update_membership_status

def register_payment(member_id, membership_id, amount):
    """
    Registra un pago y activa la membresía asociada.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Insertar el pago
        cursor.execute("""
            INSERT INTO payments (member_id, membership_id, amount, payment_status)
            VALUES (?, ?, ?, 'paid')
        """, (member_id, membership_id, amount))

        # Al registrar un pago completado, nos aseguramos de que la membresía esté activa
        update_membership_status(membership_id, "active")

        conn.commit()
        return True
    except Exception as e:
        print(f"Error registering payment: {e}")
        if conn: conn.rollback()
        return False
    finally:
        if conn: conn.close()

def get_payments_by_member(member_id):
    """Recupera el historial de pagos de un miembro específico."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM payments 
            WHERE member_id = ? 
            ORDER BY payment_date DESC
        """, (member_id,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error fetching payments: {e}")
        return []
    finally:
        if conn: conn.close()