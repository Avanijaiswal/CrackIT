from database.connection import Database
from models.company import Company


class CompanyDAO:
    def find_by_name(self, name):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM companies WHERE name = %s"
        try:
            cursor.execute(query, (name,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Company(id=row["id"], name=row["name"])
        finally:
            cursor.close()
            conn.close()

    def insert(self, name):
        db = Database()
        conn = db.connect()
        if conn is None:
            return None

        cursor = conn.cursor()
        query = "INSERT INTO companies (name) VALUES (%s)"
        try:
            cursor.execute(query, (name,))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()