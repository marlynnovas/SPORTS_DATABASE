from database.connection import get_connection


class MembershipService:

    @staticmethod
    def get_all_memberships():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ms.*,
                   m.first_name,
                   m.last_name,
                   p.name AS plan_name,
                   p.price
            FROM memberships ms
            JOIN members m ON ms.member_id = m.id
            JOIN plans p   ON ms.plan_id   = p.id
            ORDER BY ms.id DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def create_membership(member_id, plan_id, start_date, end_date, status="active"):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO memberships (member_id, plan_id, start_date, end_date, status)
                   VALUES (?, ?, ?, ?, ?)""",
                (member_id, plan_id, start_date, end_date, status),
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating membership: {e}")
            return None
        finally:
            conn.close()
