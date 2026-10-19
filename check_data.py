from database.connection import Database

conn = Database().connect()
if conn is None:
    raise SystemExit("Could not connect")

cur = conn.cursor()

for table in ["users", "companies", "experiences", "rounds", "questions", "likes", "comments"]:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"{table}: {cur.fetchone()[0]} rows")

print("\n--- Users (no passwords) ---")
cur.execute("SELECT id, name, email, contributor_score FROM users")
for row in cur.fetchall():
    print(row)

print("\n--- Experiences ---")
cur.execute("SELECT id, user_id, company_id, role, outcome, is_anonymous FROM experiences")
for row in cur.fetchall():
    print(row)

print("\n--- Questions ---")
cur.execute("SELECT id, round_id, question_text, topic FROM questions")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()