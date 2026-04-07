from database.connection import get_connection

class AccessService:
    @staticmethod
    def get_recent_logs(limit=20):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT al.*, 
                   m.first_name, 
                   m.last_name
            FROM access_logs al
            JOIN members m ON al.member_id = m.id
            ORDER BY al.access_time DESC
            LIMIT ?
        """
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def log_access(member_id, granted, message=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO access_logs (member_id, granted, message) VALUES (?, ?, ?)",
                (member_id, granted, message)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error logging access: {e}")
            return False
        finally:
            conn.close()
