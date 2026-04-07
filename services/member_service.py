from database.connection import get_connection

class MemberService:
    @staticmethod
    def create_member(first_name, last_name, email, phone):
        """
        Registra un nuevo miembro. Concatenamos nombres para cumplir con el esquema (full_name).
        """
        full_name = f"{first_name} {last_name}".strip()
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO members (full_name, phone, email)
                VALUES (?, ?, ?)
            """, (full_name, phone, email))

            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating member: {e}")
            if conn: conn.rollback()
            return None
        finally:
            if conn: conn.close()

    @staticmethod
    def get_all_members():
        """Recupera la lista completa de miembros con datos de membresía."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Usamos JOINs similares a develop para dar más info a la UI
            cursor.execute("""
                SELECT m.*,
                       ms.status   AS membership_status,
                       ms.end_date AS end_date,
                       p.name      AS plan_name
                FROM members m
                LEFT JOIN memberships ms ON m.id = ms.member_id
                LEFT JOIN plans p        ON ms.plan_id = p.id
                ORDER BY m.full_name ASC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching members: {e}")
            return []
        finally:
            if conn: conn.close()

    @staticmethod
    def search_members(query):
        """Busca miembros por nombre o correo."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            search_pattern = f"%{query}%"
            cursor.execute("""
                SELECT m.*,
                       ms.status   AS membership_status,
                       ms.end_date AS end_date,
                       p.name      AS plan_name
                FROM members m
                LEFT JOIN memberships ms ON m.id = ms.member_id
                LEFT JOIN plans p        ON ms.plan_id = p.id
                WHERE m.full_name LIKE ? OR m.email LIKE ?
                ORDER BY m.full_name ASC
            """, (search_pattern, search_pattern))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error searching members: {e}")
            return []
        finally:
            if conn: conn.close()

    @staticmethod
    def count_members():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM members")
            count = cursor.fetchone()[0]
            return count
        except:
            return 0
        finally:
            if conn: conn.close()

    @staticmethod
    def count_by_status(status: str) -> int:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM memberships WHERE status = ?", (status,)
            )
            count = cursor.fetchone()[0]
            return count
        except:
            return 0
        finally:
            if conn: conn.close()
