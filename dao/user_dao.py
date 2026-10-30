from database.connection import Database
from models.user import User
from mysql.connector import Error


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

    def add_points(self, user_id, points):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor()
        query = "UPDATE users SET contributor_score = GREATEST(contributor_score + %s, 0) WHERE id = %s"
        try:
            cursor.execute(query, (points, user_id))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    def add_points_to_experience_owner(self, experience_id, points, exclude_user_id):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor()
        query = """
            UPDATE users
            SET contributor_score = GREATEST(contributor_score + %s, 0)
            WHERE id = (SELECT user_id FROM experiences WHERE id = %s)
              AND id != %s
        """
        try:
            cursor.execute(query, (points, experience_id, exclude_user_id))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    def find_top_contributors(self, limit=20):
        db = Database()
        conn = db.connect()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT name, contributor_score
            FROM users
            WHERE contributor_score > 0
            ORDER BY contributor_score DESC, name ASC
            LIMIT %s
        """
        try:
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def is_admin(self, user_id):
        db = Database()
        conn = db.connect()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT is_admin FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            return bool(row and row[0])
        except Error as e:
            print(f"Could not check admin status: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def find_all(self):
        db = Database()
        conn = db.connect()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id, name, email, contributor_score, is_admin
            FROM users
            ORDER BY id DESC
        """
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()