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
    def create_member(first_name, last_name, email, phone, sport=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO members (first_name, last_name, email, phone, sport) VALUES (?, ?, ?, ?, ?)",
                (first_name, last_name, email, phone, sport),
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating member: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update_member(member_id, first_name, last_name, email, phone, sport=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE members SET first_name=?, last_name=?, email=?, phone=?, sport=? WHERE id=?",
                (first_name, last_name, email, phone, sport, member_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating member: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete_member(member_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Also delete memberships of this member
            cursor.execute("DELETE FROM memberships WHERE member_id=?", (member_id,))
            cursor.execute("DELETE FROM members WHERE id=?", (member_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting member: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def update_membership_status(member_id: int, status: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE memberships 
                SET status = ? 
                WHERE id = (SELECT id FROM memberships WHERE member_id = ? ORDER BY id DESC LIMIT 1)
            """, (status, member_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating member status: {e}")
            return False
        finally:
            conn.close()
