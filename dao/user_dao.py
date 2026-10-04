from database.connection import Database
from models.user import User


class UserDAO:
    def insert(self, name, email, password_hash):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor()
        query = "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (name, email, password_hash))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def find_by_email(self, email):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s"
        try:
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            if row is None:
                return None
            return User(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                password_hash=row["password_hash"],
                contributor_score=row["contributor_score"]
            )
        finally:
            cursor.close()
            conn.close()

    def find_by_id(self, user_id):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE id = %s"
        try:
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return User(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                password_hash=row["password_hash"],
                contributor_score=row["contributor_score"]
            )
        finally:
            cursor.close()
            conn.close()