from database.connection import get_connection

def create_plan(name, duration_days, price):
    """Crea un nuevo plan de membresía."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO plans (name, duration_days, price)
            VALUES (?, ?, ?)
        """, (name, duration_days, price))

        conn.commit()
    except Exception as e:
        print(f"Error creating plan: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()


def get_all_plans():
    """Obtiene todos los planes configurados."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM plans")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error fetching plans: {e}")
        return []
    finally:
        if conn: conn.close()