from database.connection import Database
from models.round import Round


class RoundDAO:
    def insert(self, experience_id, round_number, round_type):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor()
        query = """
            INSERT INTO rounds (experience_id, round_number, round_type)
            VALUES (%s, %s, %s)
        """
        try:
            cursor.execute(query, (experience_id, round_number, round_type))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def find_by_experience_id(self, experience_id):
        db = Database()
        conn = db.connect()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM rounds WHERE experience_id = %s ORDER BY round_number"
        try:
            cursor.execute(query, (experience_id,))
            rows = cursor.fetchall()
            return [
                Round(id=r["id"], experience_id=r["experience_id"],
                      round_number=r["round_number"], round_type=r["round_type"])
                for r in rows
            ]
        finally:
            cursor.close()
            conn.close()