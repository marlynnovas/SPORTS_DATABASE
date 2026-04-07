from database.connection import get_connection


class MemberService:

    @staticmethod
    def get_all_members():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*,
                   ms.status   AS membership_status,
                   ms.end_date AS end_date,
                   p.name      AS plan_name
            FROM members m
            LEFT JOIN memberships ms ON m.id = ms.member_id
            LEFT JOIN plans p        ON ms.plan_id = p.id
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def count_members():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM members")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def count_by_status(status: str) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM memberships WHERE status = ?", (status,)
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def count_no_plan() -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM members m
            LEFT JOIN memberships ms ON m.id = ms.member_id
            WHERE ms.id IS NULL
        """)
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def count_renewals_this_month() -> int:
        """Members whose membership end_date falls in the current month."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM memberships
            WHERE strftime('%Y-%m', end_date) = strftime('%Y-%m', 'now')
        """)
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def create_member(first_name, last_name, email, phone):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO members (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)",
                (first_name, last_name, email, phone),
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating member: {e}")
            return None
        finally:
            conn.close()
