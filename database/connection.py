import os
import mysql.connector
from mysql.connector import Error, pooling
from dotenv import load_dotenv

load_dotenv()

# project root = one folder above database/, where ca.pem lives
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_pool = None


def _get_pool():
    global _pool
    if _pool is None:
        config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
            "connection_timeout": 10,
        }

        # Only used online. Locally DB_SSL_CA is not set, so nothing changes.
        ca_file = os.getenv("DB_SSL_CA")
        if ca_file:
            config["ssl_ca"] = os.path.join(PROJECT_ROOT, ca_file)
            config["ssl_verify_cert"] = True

        _pool = pooling.MySQLConnectionPool(
            pool_name="crackit_pool",
            pool_size=3,
            **config
        )
    return _pool


class Database:
    def connect(self):
        try:
            return _get_pool().get_connection()
        except Error as e:
            print(f"Error Connecting to MySQL : {e}")
            return None