from database import get_connection
from models import Plan

def create_plan(plan: Plan):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO plans (name, duration_days, price)
        VALUES (?, ?, ?)
    """, (plan.name, plan.duration_days, plan.price))

    conn.commit()
    conn.close()


def get_all_plans():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM plans")
    rows = cursor.fetchall()

    conn.close()
    return rows