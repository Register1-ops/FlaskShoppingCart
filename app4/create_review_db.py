import sqlite3


# Create the reviews table if it doesn't exist

conn = sqlite3.connect('reviews_new.db')  # Connecting to the database
cursor = conn.cursor()  # Creating a cursor object to execute SQL queries

cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews_new (
        review_num INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        review TEXT NOT NULL,
        rating INTEGER NOT NULL
    )
''')
conn.commit()
conn.close()

