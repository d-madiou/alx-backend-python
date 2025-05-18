import contextlib
import mysql.connector

def stream_users_in_batches(batch_size):
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
        cursor.execute('SELECT * FROM user_data')

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        with contextlib.suppress(Exception):
            if cursor:
                cursor.close()
            if connection:
                connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filter_users = (user for user in batch if user['age'] > 25 )
        for user in filter_users:
          yield user
