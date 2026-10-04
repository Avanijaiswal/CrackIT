from database.connection import Database

db = Database()
connection = db.connect()

if connection is not None and connection.is_connected():
    print("✅ Successfully connected to the crackit database!")
    connection.close()
else:
    print("❌ Connection failed. Check your .env values and MySQL server.")