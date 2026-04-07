from database.connection import get_connection
from services.membership_service import MembershipService

class AccessService:
    @staticmethod
    def validate_access(member_id):
        """
        Valida el acceso de un miembro y registra el intento.
        Versión unificada para la UI de develop y el motor robusto.
        """
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            membership = MembershipService.get_active_membership(member_id)

            if not membership:
                result = "denied"
                message = "Sin membresía registrada"
            else:
                status = MembershipService.refresh_membership_status(membership)
                if status == "active":
                    result = "granted"
                    message = "Acceso Permitido"
                else:
                    result = "denied"
                    message = f"Membresía {status}"

            # Registrar en access_logs (usando columnas nuevas: result, access_date, access_time)
            cursor.execute("""
                INSERT INTO access_logs (member_id, result, message)
                VALUES (?, ?, ?)
            """, (member_id, result, message))

            conn.commit()
            return {"result": result, "message": message}
        except Exception as e:
            print(f"Error in access validation: {e}")
            return {"result": "denied", "message": "Error de sistema"}
        finally:
            if conn: conn.close()

    @staticmethod
    def get_recent_logs(limit: int = 50):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT al.id,
                       al.access_date || ' ' || al.access_time as access_time,
                       al.result,
                       al.message,
                       m.full_name
                FROM access_logs al
                JOIN members m ON al.member_id = m.id
                ORDER BY al.id DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching logs: {e}")
            return []
        finally:
            if conn: conn.close()

    @staticmethod
    def count_today() -> int:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM access_logs WHERE access_date = date('now')")
            return cursor.fetchone()[0]
        except: return 0
        finally:
            if conn: conn.close()

    @staticmethod
    def count_granted_today() -> int:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM access_logs WHERE access_date = date('now') AND result = 'granted'")
            return cursor.fetchone()[0]
        except: return 0
        finally:
            if conn: conn.close()

    @staticmethod
    def count_denied_today() -> int:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM access_logs WHERE access_date = date('now') AND result = 'denied'")
            return cursor.fetchone()[0]
        except: return 0
        finally:
            if conn: conn.close()
