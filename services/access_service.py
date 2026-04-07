from database.connection import get_connection


class AccessService:

    @staticmethod
    def get_recent_logs(limit: int = 50):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT al.id,
                   al.access_time,
                   al.granted,
                   al.message,
                   m.first_name,
                   m.last_name
            FROM access_logs al
            JOIN members m ON al.member_id = m.id
            ORDER BY al.access_time DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def count_today() -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM access_logs
            WHERE date(access_time) = date('now')
        """)
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def count_granted_today() -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM access_logs
            WHERE date(access_time) = date('now') AND granted = 1
        """)
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def count_denied_today() -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM access_logs
            WHERE date(access_time) = date('now') AND granted = 0
        """)
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def count_active_now() -> int:
        """Members who entered but haven't exited in the last 4 hours."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(DISTINCT member_id) FROM access_logs
            WHERE granted = 1
              AND access_time >= datetime('now', '-4 hours')
        """)
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def peak_hour_today() -> str:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%H', access_time) AS hr, COUNT(*) AS cnt
            FROM access_logs
            WHERE date(access_time) = date('now')
            GROUP BY hr
            ORDER BY cnt DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        if not row:
            return "N/A"
        return f"{row['hr']}:00"

    @staticmethod
    def hourly_traffic_today():
        """Returns a list of (hour_label, count) for the current day, 6-18 h."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%H', access_time) AS hr, COUNT(*) AS cnt
            FROM access_logs
            WHERE date(access_time) = date('now')
            GROUP BY hr
        """)
        rows = cursor.fetchall()
        conn.close()
        counts = {row["hr"]: row["cnt"] for row in rows}
        return [(f"{h}AM" if h < 12 else f"{h}PM", counts.get(f"{h:02d}", 0))
                for h in range(6, 19)]

    @staticmethod
    def week_outcome_counts():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                SUM(CASE WHEN granted=1 THEN 1 ELSE 0 END) AS granted,
                SUM(CASE WHEN granted=0 THEN 1 ELSE 0 END) AS denied
            FROM access_logs
            WHERE access_time >= datetime('now', '-7 days')
        """)
        row = cursor.fetchone()
        conn.close()
        granted = row["granted"] or 0
        denied  = row["denied"]  or 0
        total   = granted + denied or 1
        return granted, denied, total

    @staticmethod
    def log_access(member_id: int, granted: bool, message: str = None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO access_logs (member_id, granted, message) VALUES (?, ?, ?)",
                (member_id, int(granted), message),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error logging access: {e}")
            return False
        finally:
            conn.close()
