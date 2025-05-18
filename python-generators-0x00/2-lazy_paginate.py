import contextlib
import mysql.connector

def paginate_users(page_size, offset):
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
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    finally:
        with contextlib.suppress(Exception):
            if cursor:
                cursor.close()
            if connection:
                connection.close()

def lazy_paginate(page_size):
    offset = 0
    while True:
        batch = paginate_users(page_size, offset)
        if not batch:
            break
        for user in batch:
            yield user
        offset += page_size
