import mysql.connector

def stream_user():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234',
            database='alx_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_data')

        for row in cursor:
            yield row
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        try:
            cursor.close()
            connection.close()
        except Exception:
            pass