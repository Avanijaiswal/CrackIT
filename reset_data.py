from database.connection import Database


def reset_all_data():
    
    db = Database()
    connection = db.connect()

    if connection is None:
        print("Could not reset data — no database connection.")
        return

    cursor = connection.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        tables = ["likes", "comments", "questions", "rounds", "experiences", "companies", "users"]
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table}")
            print(f"Cleared table: {table}")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        connection.commit()
        print("\n All data cleared. Tables are empty, structure intact.")

    except Exception as e:
        print(f"Error resetting data: {e}")
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    confirm = input("⚠️This will delete ALL data in every table. Type 'yes' to confirm: ")
    if confirm.strip().lower() == "yes":
        reset_all_data()
    else:
        print("Cancelled. No data was deleted.")