import sys
from database.connection import Database

if len(sys.argv) != 2:
    raise SystemExit("Usage: python make_admin.py your@email.com")

email = sys.argv[1]
conn = Database().connect()
if conn is None:
    raise SystemExit("Could not connect")

cur = conn.cursor()
try:
    cur.execute("ALTER TABLE users ADD COLUMN is_admin TINYINT(1) NOT NULL DEFAULT 0")
    conn.commit()
    print("Added is_admin column.")
except Exception as e:
    print("Column step skipped:", e)

cur.execute("UPDATE users SET is_admin = 1 WHERE email = %s", (email,))
conn.commit()
print("Rows updated:", cur.rowcount)
cur.close()
conn.close()