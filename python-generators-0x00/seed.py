import mysql.connector
import csv
import uuid

def connect_db():
    """Connects to the MySQL server."""
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
    """Creates the database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS alx_prodev")
        print("Database ALX_prodev created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234',
            database='alx_prodev'
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None

def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields."""
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5,2) NOT NULL,
                INDEX (user_id)
            )
        """)
        connection.commit()
        print("Table user_data created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data):
    """Inserts data into the database if it does not exist (based on email uniqueness)."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, data)
        connection.commit()
    except Exception as e:
        print(f"Error inserting data {data}: {e}")

def populate_from_csv(connection, csv_file):
    """Reads from the CSV file and populates the table using insert_data()."""
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    user_id = str(uuid.uuid4())
                    name = row["name"].strip()
                    email = row["email"].strip()
                    age = float(row["age"].strip())
                    insert_data(connection, (user_id, name, email, age))
                except Exception as e:
                    print(f"Skipping row due to error: {row}, Error: {e}")
        print("✅ Database successfully populated from CSV.")
    except FileNotFoundError:
        print(f"CSV file '{csv_file}' not found.")
    except Exception as e:
        print(f"Error reading from CSV: {e}")


# Main Execution Flow
if __name__ == "__main__":
    # Step 1: Connect to server
    conn = connect_db()
    if not conn:
        exit(1)

    # Step 2: Create DB
    create_database(conn)
    conn.close()

    # Step 3: Connect to ALX_prodev DB
    conn = connect_to_prodev()
    if not conn:
        exit(1)

    # Step 4: Create table
    create_table(conn)

    # Step 5: Populate from CSV
    populate_from_csv(conn, 'user_data.csv')

    conn.close()
