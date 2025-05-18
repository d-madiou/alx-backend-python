import contextlib
import mysql.connector

def stream_user_ages():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234',
            database='alx_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")

        for row in cursor:
            yield row['age']

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        with contextlib.suppress(Exception):
            if cursor:
                cursor.close()
            if connection:
                connection.close()

def calculate_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    calculate_average_age()
