from database.connection import get_connection
from services.membership_service import get_active_membership, refresh_membership_status

def validate_access(member_id):
    """
    Valida el acceso de un miembro y registra el intento en los logs.
    Implementa la lógica de control de acceso requerida por la documentación.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        membership = get_active_membership(member_id)

        if not membership:
            result = "denied"
            message = "Sin membresía registrada"
        else:
            # refresh_membership_status se encarga de la proactividad (vencimiento)
            status = refresh_membership_status(membership)

            if status == "active":
                result = "granted"
                message = "Acceso Permitido"
            else:
                result = "denied"
                message = f"Membresía {status}"

        # Registrar el intento en la DB (access_logs)
        # El schema actualizado tiene access_date y access_time por separado
        cursor.execute("""
            INSERT INTO access_logs (member_id, result, message)
            VALUES (?, ?, ?)
        """, (member_id, result, message))

        conn.commit()

        return {
            "result": result,
            "message": message
        }
    except Exception as e:
        print(f"Error in access validation: {e}")
        return {
            "result": "denied",
            "message": "Error de validación de sistema"
        }
    finally:
        if conn: conn.close()