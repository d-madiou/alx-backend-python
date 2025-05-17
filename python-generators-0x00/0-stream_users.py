import contextlib
import mysql.connector

def stream_users():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234',
            database='alx_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_data')

        yield from cursor
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        with contextlib.suppress(Exception):
            cursor.close()
            connection.close()