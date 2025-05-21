import sqlite3
import functools

"""your code goes here"""
#I'm importing the previous function and in this one we already defined a function 
#that is handling the open and close database, we can ue a decorator with it
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"operation failed: {e}")
            raise
    return wrapper

#this part, the with_db decorator is wrapping the transaction decorator into it
#the transaction decorator is executing the original function (update_user email)
#the concept is bottom up
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
        #### Update user's email with automatic transaction handling

        update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
        print("user email updated")