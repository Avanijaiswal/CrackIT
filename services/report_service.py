from database.connection import Database

def get_topic_frequency(company_name):
    db = Database()
    connection = db.connect()

    if connection is None:
        print("Could not generate report — no database connection.")
        return []

    cursor = connection.cursor(dictionary = True)
    try:
        cursor.execute("""select q.topic, count(*) as topic_count
                          from questions q
                          join rounds r on q.round_id = r.id
                          join experiences e on r.experience_id = e.id
                          join companies c on e.company_id = c.id
                          where c.name = %s
                          group by q.topic
                          order by topic_count desc""",(company_name,))
        return cursor.fetchall()

    except Exception as e:
        print(f" Error genrerating topic frequency : {e}")
        return []

    finally:
        cursor.close()
        connection.close()

def get_round_type_breakdown(company_name):
    db = Database()
    connection = db.connect()

    if connection is None:
        print("Could not generate report — no database connection.")
        return []
    cursor = connection.cursor(dictionary = True)
    try:
        cursor.execute("""select r.round_type, count(*) as type_count
                          from rounds r
                          join experiences e on r.experience_id - e.id
                          join companies c on e.company_id = c.id
                          where c.name = %s
                          group by r.round_type
                          order by type_count desc
                          """,
                          (company_name,))
        results = cursor.fetchall()

        total_rounds =  sum(row["type_count"] for row in results)

        if total_rounds == 0:
             return[]

        for row in results :
            row["percentage"] = round((row["type_count"] / total_rounds) * 100, 1)

        return results

    except Exception as e:
        print(f" Error generating round type breakdown : {e}")
        return []

    finally:
        cursor.close()
        connection.close()

def get_crack_rate(company_name):

    db = Database()
    connection = db.connect()

    if connection is None:
        print("Could not calculate crack rate — no database connection.")
        return None

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT e.outcome, COUNT(*) AS outcome_count
            FROM experiences e
            JOIN companies c ON e.company_id = c.id
            WHERE c.name = %s
            GROUP BY e.outcome
            """,
            (company_name,)
        )
        results = cursor.fetchall()

        total = sum(row["outcome_count"] for row in results)

        if total == 0:
            return None

        selected_count = 0
        for row in results:
            if row["outcome"] == "Selected":
                selected_count = row["outcome_count"]

        crack_rate = round((selected_count / total) * 100, 1)

        return {
            "crack_rate": crack_rate,
            "selected_count": selected_count,
            "total_count": total
        }

    except Exception as e:
        print(f"Error calculating crack rate: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    print("--- Topic Frequency ---")
    for row in get_topic_frequency("Amazon"):
        print(f"{row['topic']}: {row['topic_count']}")

    print("\n--- Round Type Breakdown ---")
    for row in get_round_type_breakdown("Amazon"):
        print(f"{row['round_type']}: {row['type_count']} rounds ({row['percentage']}%)")