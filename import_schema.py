from database.connection import Database

with open("schema.sql", "r", encoding="utf-8") as f:
    sql = f.read().replace("\r\n", "\n")

conn = Database().connect()
if conn is None:
    raise SystemExit("Could not connect")

cur = conn.cursor()
statements = [s.strip() for s in sql.split(";\n") if s.strip()]

ok, skipped = 0, 0
for stmt in statements:
    try:
        cur.execute(stmt)
        ok += 1
    except Exception as e:
        skipped += 1
        print("SKIPPED:", stmt[:80].replace("\n", " "), "->", e)

conn.commit()
cur.execute("SHOW TABLES")
print("Tables now in Aiven:", [r[0] for r in cur.fetchall()])
print(ok, "statements ran,", skipped, "skipped")
cur.close()
conn.close()