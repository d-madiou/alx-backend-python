import mysql.connector
import csv

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234'
        )
        if connection.is_connected():
            print("Connected to MySQL server")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS alx_prodev")  # Ensure spelling consistent
        print("Database ALX_prodev created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234',
            database='alx_prodev'  # Ensure spelling consistent here too
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age INT NOT NULL
            )
        """)
        connection.commit()
        print("Table user_data created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

if __name__ == "__main__":
    conn = connect_db()
    if conn is None:
        print("Failed to connect to MySQL server.")
        exit(1)

    create_database(conn)
    conn.close()

    conn = connect_to_prodev()
    if conn is None:
        print("Failed to connect to ALX_prodev database.")
        exit(1)

    create_table(conn)
    conn.close()
