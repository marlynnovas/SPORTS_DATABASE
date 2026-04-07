import sqlite3
import os
from database.connection import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if empty
    cursor.execute("SELECT count(*) FROM members")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("Seeding database with initial data...")
        # Add members
        members = [
            ("Juan", "Perez", "juan@example.com", "8095551234"),
            ("Maria", "Rodriguez", "maria@example.com", "8295554321"),
            ("Pedro", "García", "pedro@example.com", "8495556789")
        ]
        cursor.executemany("INSERT INTO members (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)", members)
        
        # Add plans
        plans = [
            ("Monthly Basic", 1500.0, 1),
            ("Quarterly Standard", 4000.0, 3),
            ("Yearly Premium", 15000.0, 12)
        ]
        cursor.executemany("INSERT INTO plans (name, price, duration_months) VALUES (?, ?, ?)", plans)
        
        # Add memberships
        cursor.execute("SELECT id FROM members")
        m_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT id FROM plans")
        p_ids = [row[0] for row in cursor.fetchall()]
        
        import datetime
        today = datetime.date.today()
        month_later = today + datetime.timedelta(days=30)
        
        for m_id in m_ids:
            cursor.execute("INSERT INTO memberships (member_id, plan_id, start_date, end_date, status) VALUES (?, ?, ?, ?, 'active')", 
                           (m_id, p_ids[0], today.isoformat(), month_later.isoformat()))
            
            # Add some access logs
            cursor.execute("INSERT INTO access_logs (member_id, access_time, granted, message) VALUES (?, datetime('now', '-1 hour'), 1, 'Welcome back!')", (m_id,))
            cursor.execute("INSERT INTO access_logs (member_id, access_time, granted, message) VALUES (?, datetime('now', '-2 hours'), 1, 'Valid membership')", (m_id,))
            
        conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_data()
