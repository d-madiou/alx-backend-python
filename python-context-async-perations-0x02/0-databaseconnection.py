import sqlite3

class DatabaseConnection:
    def __init__(self):
        self.conn = None
    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        return self.conn
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

with DatabaseConnection() as db:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    print(result)