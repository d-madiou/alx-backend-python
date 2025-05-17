#!/usr/bin/python3

seed = __import__('seed')

# Connect to the database
connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print("Connection successful.")

    connection = seed.connect_to_prodev()

if connection:
    seed.create_table(connection)
    seed.insert_data(connection, 'user_data.csv')

    cursor = connection.cursor()
    cursor.execute(
        "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';"
    )
    if result := cursor.fetchone():
        print("Database ALX_prodev is present.")

    # Use the generator to stream data
    for row in seed.stream_user_data(connection):
        print(row)
    cursor.close()
