#let's create a reusable context manager that can take a query input and handle the connection
import sqlite3


class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params if params is not None else()
        self.conn = sqlite3.connect("users.db")
        self.cursor = None

    def __enter__(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor


    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
query = "SELECT * FROM users WHERE age > ?"
params = (25,)
with ExecuteQuery(query, params) as cursor:
    rows = cursor.fetchall()
    print(rows)
