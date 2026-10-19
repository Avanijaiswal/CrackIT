import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

# project root = one folder above database/, where ca.pem lives
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Database:
    def connect(self):
        try:
            config = {
                "host": os.getenv("DB_HOST", "localhost"),
                "port": int(os.getenv("DB_PORT", "3306")),
                "user": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASSWORD"),
                "database": os.getenv("DB_NAME"),
            }

            ca_file = os.getenv("DB_SSL_CA")
            if ca_file:
                config["ssl_ca"] = os.path.join(PROJECT_ROOT, ca_file)
                config["ssl_verify_cert"] = True

            connection = mysql.connector.connect(**config)
            return connection
        except Error as e:
            print(f"Error Connecting to MySQL : {e}")
            return None