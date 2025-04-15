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
        short_description TEXT NOT NULL,
        long_description TEXT NOT NULL,
        image TEXT NOT NULL,
        environmentScore INTEGER NOT NULL
    )
''')

# List of products to insert
products = [
    ("Taylor GS Mini Acoustic Guitar", "£599", 
     "Travel-sized acoustic guitar made with responsibly-sourced wood for a rich tone.", 
     "The Taylor GS Mini is a small-bodied acoustic guitar that delivers big sound, perfect for both beginners and seasoned musicians. Despite its compact size, it offers a rich and vibrant tone thanks to Taylor’s precision craftsmanship and the use of responsibly sourced wood. The GS Mini is an excellent choice for musicians who travel or want a portable option for practicing and performing.", 
     "taylor_gs_mini.jpeg", 10),
     
    ("Squier Classic Vibe '60s Telecaster", "£429", 
     "Vintage Tele style with smooth tone and retro looks.", 
     "The Squier Classic Vibe '60s Telecaster offers all the classic Tele sound and style at an affordable price. With its vintage-inspired design, this guitar produces the bright, punchy tones that Telecasters are famous for. Perfect for rock, blues, and country players, the guitar has a comfortable, modern neck and comes with vintage-style hardware for an authentic look and feel.", 
     "squier_telecaster.jpeg", 19),
     
    ("Fender Player Stratocaster", "£629", 
     "Iconic Stratocaster sound with a modern, sleek design.", 
     "The Fender Player Stratocaster is a modern twist on the iconic Stratocaster design. Known for its bright, clear tones and versatile pickup selection, the Player Stratocaster is perfect for a wide variety of musical genres, including rock, pop, and blues. Its sleek, contoured body and responsive neck make it an excellent choice for players of all levels.", 
     "fender_strat.jpeg", 17),

     ("Ibanez GRX70QA Electric Guitar", "£179", 
     "Affordable electric guitar with smooth playability and great tones.", 
     "The Ibanez GRX70QA is an excellent entry-level electric guitar, offering great playability and solid tones at an affordable price. The guitar features a sleek, lightweight body with a powerful, smooth sound from its dual humbucker pickups. Whether you're just starting out or looking for a budget-friendly electric guitar, the GRX70QA offers a high-quality playing experience.", 
     "ibanez_grx70qa.jpeg", 14),
     
    ("Boss RC-5 Loop Station", "£199", 
     "Compact looper with 13 hours of stereo recording and rhythm backing.", 
     "The Boss RC-5 Loop Station is a compact, powerful looper designed for musicians who want to layer sounds and create complex musical compositions on the fly. With 13 hours of stereo recording, over 50 built-in rhythms, and the ability to sync with external devices, the RC-5 is perfect for solo performers, songwriters, and experimental musicians. It also features USB connectivity for easy backup and sound editing.", 
     "boss_rc5.jpeg", 11),
     
    ("TC Electronic Ditto Looper", "£99", 
     "Simple and high-quality looper for creating endless loops on stage.", 
     "The TC Electronic Ditto Looper is a compact, user-friendly looper that offers high-quality sound and ease of use. It’s perfect for live performances, allowing musicians to create seamless loops with the touch of a button. Despite its small size, the Ditto Looper packs a punch, offering 5 minutes of loop time and the option to undo/redo recordings. Ideal for guitarists and other musicians looking to add layers to their sound.", 
     "tc_electronic_ditto.jpeg", 6),
     
    ("Yamaha P-225 Digital Piano", "£629", 
     "A slim, high-performance digital piano with expressive keys and realistic sound.", 
     "The Yamaha P-225 Digital Piano combines portability with professional-grade sound. It features a GHS weighted action keyboard for a realistic piano feel and boasts an impressive range of voices and effects. The compact design makes it easy to transport, while the realistic piano sound offers depth and richness, making it an excellent option for beginners and experienced players alike.", 
     "yamaha_p225.jpeg", 16),
     
    ("Alesis Nitro Mesh Kit", "£379", 
     "Affordable electronic drum kit with mesh heads for quiet practice.", 
     "The Alesis Nitro Mesh Kit is an affordable, entry-level electronic drum kit with mesh drum heads that provide a more realistic, quieter playing experience compared to rubber pads. This kit includes everything you need to get started, including a module with a wide variety of drum sounds and 385 percussion voices. It’s ideal for new drummers who want to practice quietly or drummers with limited space.", 
     "alesis_nitro.jpeg", 25),
     
    ("Fender Mustang Micro", "£129", 
     "Compact and portable headphone amp with built-in effects.", 
     "The Fender Mustang Micro is a revolutionary, portable headphone amplifier that brings Fender’s famous tones straight to your ears. With built-in effects and amp models, it’s perfect for practice or jamming on the go. Whether you’re looking to practice at home or take it with you on the road, the Mustang Micro offers convenient, high-quality sound in a compact form.", 
     "fender_mustang_micro.jpeg", 7)
]

# Insert products into the table
cursor.executemany('INSERT INTO products (name, price, short_description, long_description, image, environmentScore) VALUES (?, ?, ?, ?, ?, ?)', products)

# Commit and close the database connection
conn.commit()
conn.close()

print("Database created and populated successfully!")
