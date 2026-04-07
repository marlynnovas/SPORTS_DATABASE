from database.connection import get_connection

class MemberService:
    @staticmethod
    def get_all_members():
        conn = get_connection()
        cursor = conn.cursor()
        # Join with memberships to get the status and plan
        query = """
            SELECT m.*, 
                   ms.status as membership_status, 
                   ms.end_date, 
                   p.name as plan_name
            FROM members m
            LEFT JOIN memberships ms ON m.id = ms.member_id
            LEFT JOIN plans p ON ms.plan_id = p.id
        """
        cursor.execute(query)
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
    def create_member(first_name, last_name, email, phone):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO members (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)",
                (first_name, last_name, email, phone)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating member: {e}")
            return None
        finally:
            conn.close()
