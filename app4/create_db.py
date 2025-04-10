import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price TEXT NOT NULL,
        description TEXT NOT NULL,
        image TEXT NOT NULL,
        environmentScore INTEGER NOT NULL
    )
''')

# List of products to insert
products = [
    ("Portable Power Bank (20,000mAh)", "£34.99", "Keep your devices charged on the go with this high-capacity fast-charging power bank.", "headphones.jpeg", "1"),
    ("Multi-Port USB-C Hub", "£44.99", "Expand your laptop’s capabilities with this 7-in-1 USB-C hub featuring HDMI, USB, and SD card slots.", "Multi-Port_USB-C_Hub.jpeg", "2"),
    ("Mini Projector (1080p HD)", "£149.99", "Transform any room into a cinema with this portable, high-resolution projector.", "Projector.jpeg", "3")
]

# Insert products into the table
cursor.executemany('INSERT INTO products (name, price, description, image, environmentScore) VALUES (?, ?, ?, ?, ?)', products)

# Commit and close the database connection
conn.commit()
conn.close()

print("Database created and populated successfully!")
