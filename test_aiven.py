from database.connection import Database

conn = Database().connect()
if conn is None:
    print("FAILED to connect")
else:
    cur = conn.cursor()
    cur.execute("SELECT VERSION()")
    print("Connected! MySQL version:", cur.fetchone()[0])
    cur.close()
    conn.close()