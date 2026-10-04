import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

class Database:
    def connect(self):
        try:
            connection = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                port = int(os.getenv("DB_PORT")),
                user = os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            return connection
        except Error as e:
            print(f"Error Connecting to MySQL : {e}")
            return None


        
