from database.connection import get_connection

def create_member(full_name, phone, email):
    """Registra un nuevo miembro en la base de datos."""
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


def get_all_members():
    """Recupera la lista completa de miembros."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM members ORDER BY full_name ASC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error fetching members: {e}")
        return []
    finally:
        if conn: conn.close()


def search_members(query):
    """
    Busca miembros por nombre o correo electrónico.
    Cumple con el requisito de filtrado/búsqueda.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT * FROM members 
            WHERE full_name LIKE ? OR email LIKE ?
            ORDER BY full_name ASC
        """, (search_pattern, search_pattern))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error searching members: {e}")
        return []
    finally:
        if conn: conn.close()