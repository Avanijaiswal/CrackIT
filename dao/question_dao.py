from database.connection import Database
from models.question import Question


class QuestionDAO:
    def insert(self, round_id, question_text, topic):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor()
        query = """
            INSERT INTO questions (round_id, question_text, topic)
            VALUES (%s, %s, %s)
        """
        try:
            cursor.execute(query, (round_id, question_text, topic))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def find_by_round_id(self, round_id):
        db = Database()
        conn = db.connect()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM questions WHERE round_id = %s"
        try:
            cursor.execute(query, (round_id,))
            rows = cursor.fetchall()
            return [
                Question(id=r["id"], round_id=r["round_id"],
                          question_text=r["question_text"], topic=r["topic"])
                for r in rows
            ]
        finally:
            cursor.close()
            conn.close()