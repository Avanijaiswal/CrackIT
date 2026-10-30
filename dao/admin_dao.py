from database.connection import Database
from mysql.connector import Error

COUNT_TABLES = ["experiences", "questions", "comments", "likes", "users", "companies"]

SECTION_QUERIES = {
    "experiences": """
        SELECT e.id, c.name AS company, e.role, e.outcome, e.is_anonymous, u.name AS user_name
        FROM experiences e
        JOIN companies c ON e.company_id = c.id
        JOIN users u ON e.user_id = u.id
        ORDER BY e.id DESC
    """,
    "questions": """
        SELECT q.id, c.name AS company, r.round_number, r.round_type, q.question_text, q.topic
        FROM questions q
        JOIN rounds r ON q.round_id = r.id
        JOIN experiences e ON r.experience_id = e.id
        JOIN companies c ON e.company_id = c.id
        ORDER BY q.id DESC
    """,
    "comments": """
        SELECT cm.id, c.name AS company, e.role, u.name AS user_name, cm.comment_text
        FROM comments cm
        JOIN experiences e ON cm.experience_id = e.id
        JOIN companies c ON e.company_id = c.id
        JOIN users u ON cm.user_id = u.id
        ORDER BY cm.id DESC
    """,
    "likes": """
        SELECT l.id, u.name AS user_name, c.name AS company, e.role
        FROM likes l
        JOIN users u ON l.user_id = u.id
        JOIN experiences e ON l.experience_id = e.id
        JOIN companies c ON e.company_id = c.id
        ORDER BY l.id DESC
    """,
    "users": """
        SELECT u.id, u.name, u.email, u.contributor_score, u.is_admin,
               (SELECT COUNT(*) FROM experiences e WHERE e.user_id = u.id) AS exp_count
        FROM users u
        ORDER BY u.id DESC
    """,
    "companies": """
        SELECT c.id, c.name,
               (SELECT COUNT(*) FROM experiences e WHERE e.company_id = c.id) AS exp_count
        FROM companies c
        ORDER BY c.name
    """,
}

# score = 10 per experience posted + 2 per like received from someone else
RECALC_SQL = """
    UPDATE users u
    SET contributor_score =
        10 * (SELECT COUNT(*) FROM experiences e WHERE e.user_id = u.id)
      + 2 * (SELECT COUNT(*) FROM likes l
             JOIN experiences e ON l.experience_id = e.id
             WHERE e.user_id = u.id AND l.user_id != u.id)
"""


class AdminDAO:
    def get_counts(self):
        conn = Database().connect()
        if conn is None:
            return {}
        cursor = conn.cursor()
        counts = {}
        try:
            for table in COUNT_TABLES:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                counts[table] = cursor.fetchone()[0]
            return counts
        finally:
            cursor.close()
            conn.close()

    def list_section(self, section):
        query = SECTION_QUERIES.get(section)
        if query is None:
            return []
        conn = Database().connect()
        if conn is None:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def _delete_experience(self, cursor, experience_id):
        cursor.execute(
            "DELETE FROM questions WHERE round_id IN "
            "(SELECT id FROM rounds WHERE experience_id = %s)",
            (experience_id,)
        )
        cursor.execute("DELETE FROM rounds WHERE experience_id = %s", (experience_id,))
        cursor.execute("DELETE FROM likes WHERE experience_id = %s", (experience_id,))
        cursor.execute("DELETE FROM comments WHERE experience_id = %s", (experience_id,))
        cursor.execute("DELETE FROM experiences WHERE id = %s", (experience_id,))

    def delete_item(self, kind, item_id):
        conn = Database().connect()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            if kind == "experience":
                self._delete_experience(cursor, item_id)
                cursor.execute(RECALC_SQL)

            elif kind == "user":
                cursor.execute("SELECT is_admin FROM users WHERE id = %s", (item_id,))
                row = cursor.fetchone()
                if row is None or row[0]:
                    return False  # no such user, or an admin: refuse
                cursor.execute("SELECT id FROM experiences WHERE user_id = %s", (item_id,))
                for (exp_id,) in cursor.fetchall():
                    self._delete_experience(cursor, exp_id)
                cursor.execute("DELETE FROM likes WHERE user_id = %s", (item_id,))
                cursor.execute("DELETE FROM comments WHERE user_id = %s", (item_id,))
                cursor.execute("DELETE FROM users WHERE id = %s", (item_id,))
                cursor.execute(RECALC_SQL)

            elif kind == "company":
                cursor.execute("SELECT id FROM experiences WHERE company_id = %s", (item_id,))
                for (exp_id,) in cursor.fetchall():
                    self._delete_experience(cursor, exp_id)
                cursor.execute("DELETE FROM companies WHERE id = %s", (item_id,))
                cursor.execute(RECALC_SQL)

            elif kind == "like":
                cursor.execute("DELETE FROM likes WHERE id = %s", (item_id,))
                cursor.execute(RECALC_SQL)

            elif kind == "comment":
                cursor.execute("DELETE FROM comments WHERE id = %s", (item_id,))

            elif kind == "question":
                cursor.execute("DELETE FROM questions WHERE id = %s", (item_id,))

            else:
                return False

            conn.commit()
            return True
        except Error as e:
            conn.rollback()
            print(f"Could not delete {kind}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def set_admin(self, user_id, make_admin):
        conn = Database().connect()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET is_admin = %s WHERE id = %s", (1 if make_admin else 0, user_id))
            conn.commit()
            return True
        except Error as e:
            print(f"Could not change role: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def recalculate_points(self):
        conn = Database().connect()
        if conn is None:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(RECALC_SQL)
            conn.commit()
            return True
        except Error as e:
            print(f"Could not recalculate points: {e}")
            return False
        finally:
            cursor.close()
            conn.close()