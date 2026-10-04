from database.connection import Database
from models.experience import Experience


class ExperienceDAO:
    def insert(self, user_id, company_id, role, outcome, is_anonymous=False):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor()
        query = """
            INSERT INTO experiences (user_id, company_id, role, outcome, is_anonymous)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (user_id, company_id, role, outcome, int(is_anonymous)))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def find_by_company_name(self, company_name):
        db = Database()
        conn = db.connect()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT e.id, e.user_id, e.company_id, e.role, e.outcome,
                   e.is_anonymous, e.created_at, u.name AS user_name
            FROM experiences e
            JOIN companies c ON e.company_id = c.id
            JOIN users u ON e.user_id = u.id
            WHERE c.name = %s
            ORDER BY e.created_at DESC
        """
        try:
            cursor.execute(query, (company_name,))
            rows = cursor.fetchall()

            experiences = []
            for row in rows:
                exp = Experience(
                    id=row["id"],
                    user_id=row["user_id"],
                    company_id=row["company_id"],
                    role=row["role"],
                    outcome=row["outcome"],
                    is_anonymous=row["is_anonymous"],
                    created_at=row["created_at"]
                )
                exp.user_name = row["user_name"]
                experiences.append(exp)

            return experiences
        finally:
            cursor.close()
            conn.close()