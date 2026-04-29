from database.connection import get_connection


class PaymentService:

    @staticmethod
    def get_all_payments(limit: int = 100):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT py.id,
                   py.amount,
                   py.payment_date,
                   py.status,
                   m.first_name,
                   m.last_name,
                   p.name AS plan_name
            FROM payments py
            JOIN memberships ms ON py.membership_id = ms.id
            JOIN members m      ON ms.member_id = m.id
            JOIN plans p        ON ms.plan_id   = p.id
            ORDER BY py.payment_date DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def revenue_mtd() -> float:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) FROM payments
            WHERE strftime('%Y-%m', payment_date) = strftime('%Y-%m', 'now')
              AND status = 'completed'
        """)
        val = cursor.fetchone()[0]
        conn.close()
        return val

    @staticmethod
    def count_by_status(status: str) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM payments WHERE status = ?", (status,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def average_amount() -> float:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(AVG(amount), 0) FROM payments")
        val = cursor.fetchone()[0]
        conn.close()
        return val

    @staticmethod
    def count_this_month() -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM payments
            WHERE strftime('%Y-%m', payment_date) = strftime('%Y-%m', 'now')
        """)
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def monthly_revenue(months: int = 6):
        """Returns list of (month_label, total) for chart bars."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%Y-%m', payment_date) AS month,
                   SUM(amount) AS total
            FROM payments
            WHERE status = 'completed'
            GROUP BY month
            ORDER BY month DESC
            LIMIT ?
        """, (months,))
        rows = cursor.fetchall()
        conn.close()
        # Reverse so oldest first
        return [(r["month"], r["total"]) for r in reversed(rows)]

    @staticmethod
    def method_distribution():
        """
        Payments table has no 'method' column yet. Returns empty list for now.
        Once the schema is extended with a method column this will return real data.
        """
        return []

    @staticmethod
    def create_payment(membership_id: int, amount: float, status: str = "completed"):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO payments (membership_id, amount, status) VALUES (?, ?, ?)",
                (membership_id, amount, status),
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating payment: {e}")
            return None
        finally:
            conn.close()
    @staticmethod
    def update_payment_status(payment_id: int, status: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE payments SET status = ? WHERE id = ?", (status, payment_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating payment status: {e}")
            return False
        finally:
            conn.close()
    @staticmethod
    def delete_payment(payment_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting payment: {e}")
            return False
        finally:
            conn.close()
