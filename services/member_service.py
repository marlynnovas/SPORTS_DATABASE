from database.connection import get_connection

class MemberService:
    @staticmethod
    def get_all_members():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()
        conn.close()
        return rows

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
