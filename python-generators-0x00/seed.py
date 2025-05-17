import mysql.connector
import csv

# Connect to the database
def connect_db():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',  # <-- Replace with your MySQL username
            password='1234',  # <-- Replace with your MySQL password
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create the ALX_prodev database if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()

# Connect to ALX_prodev
def connect_to_prodev():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # <-- Replace with your MySQL username
        password='1234',  # <-- Replace with your MySQL password
        database='ALX_prodev'
    )

# Create the user_data table if it doesn't exist
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

# Insert data from CSV (assumes CSV format is correctly aligned with table fields)
def insert_data(connection, csv_file):
    cursor = connection.cursor()
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name), email = VALUES(email), age = VALUES(age)
                """, row)
        connection.commit()
        print(f"Data from {csv_file} inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()

# Generator for streaming rows from the user_data table
def stream_user_data(connection, batch_size=5):
    # sourcery skip: use-named-expression
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM user_data")

        while True:
            rows = cursor.fetchmany(batch_size)
            if rows:
                yield from rows
            else:
                break
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")
    finally:
        cursor.close()
