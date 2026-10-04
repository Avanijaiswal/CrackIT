from database.connection import Database
from models.comment import Comment


class SocialDAO:
    def insert_comment(self, experience_id, user_id, comment_text):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor()
        query = "INSERT INTO comments (experience_id, user_id, comment_text) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (experience_id, user_id, comment_text))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def find_comments_by_experience_id(self, experience_id):
        db = Database()
        conn = db.connect()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT c.id, c.experience_id, c.user_id, c.comment_text, c.created_at,
                   u.name AS user_name
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.experience_id = %s
            ORDER BY c.created_at ASC
        """
        try:
            cursor.execute(query, (experience_id,))
            rows = cursor.fetchall()
            comments = []
            for row in rows:
                c = Comment(
                    id=row["id"], experience_id=row["experience_id"],
                    user_id=row["user_id"], comment_text=row["comment_text"],
                    created_at=row["created_at"]
                )
                c.user_name = row["user_name"]
                comments.append(c)
            return comments
        finally:
            cursor.close()
            conn.close()

    def find_like(self, user_id, experience_id):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor()
        query = "SELECT id FROM likes WHERE user_id = %s AND experience_id = %s"
        try:
            cursor.execute(query, (user_id, experience_id))
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            cursor.close()
            conn.close()

    def insert_like(self, user_id, experience_id):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor()
        query = "INSERT INTO likes (user_id, experience_id) VALUES (%s, %s)"
        try:
            cursor.execute(query, (user_id, experience_id))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def delete_like(self, like_id):
        db = Database()
        conn = db.connect()
        if conn is None:
            return

        cursor = conn.cursor()
        query = "DELETE FROM likes WHERE id = %s"
        try:
            cursor.execute(query, (like_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def count_likes(self, experience_id):
        db = Database()
        conn = db.connect()
        if conn is None:
            return 0

        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM likes WHERE experience_id = %s"
        try:
            cursor.execute(query, (experience_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            cursor.close()
            conn.close()