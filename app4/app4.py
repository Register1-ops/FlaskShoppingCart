from collections import Counter
from flask import Flask, flash, render_template, request, redirect, url_for, session  # Importing necessary Flask modules
from flask_wtf import FlaskForm  # Importing Flask-WTF for form handling
from wtforms import StringField, SubmitField  # Importing form fields from WTForms
from wtforms.validators import DataRequired, Length  # Importing validators for form validation
from flask_bootstrap import Bootstrap  # Importing Bootstrap for styling
import sqlite3  # Importing SQLite for database operations
from datetime import datetime
import re
import time 

app = Flask(__name__)  # Creating a Flask web application instance
bootstrap = Bootstrap(app)  # Initializing Flask-Bootstrap for UI styling
app.config['SECRET_KEY'] = "top secret password don't tell anyone this"  # Setting a secret key for session security

# Function to fetch all products from the SQLite database
def get_products():
    conn = sqlite3.connect('products.db')  # Connecting to the database
    cursor = conn.cursor()  # Creating a cursor object to execute SQL queries
    cursor.execute("SELECT id, name, price, short_description, long_description, image, environmentScore FROM products")  # Querying all products
    
    # Fetching all results and formatting them as dictionaries
    products = [
        {"id": row[0], "name": row[1], "price": row[2], "short_description": row[3], "long_description": row[4], "image": row[5], "environmentScore": row[6]}
        for row in cursor.fetchall()
    ]
    conn.close()  # Closing the database connection
    return products  # Returning the list of products

# Function to fetch a single product by ID
def get_product_by_id(tech_id):
    conn = sqlite3.connect('products.db')  # Connecting to the database
    cursor = conn.cursor()  # Creating a cursor object
    cursor.execute("SELECT id, name, price, short_description, long_description, image, environmentScore FROM products WHERE id = ?", (tech_id,))  # Querying a specific product
    row = cursor.fetchone()  # Fetching the result
    conn.close()  # Closing the connection
    
    # If a product exists, return it as a dictionary
    if row:
        return {"id": row[0], "name": row[1], "price": row[2], "short_description": row[3], "long_description": row[4], "image": row[5], "environmentScore": row[6]}
    return None  # Return None if product not found


# Route for the homepage displaying all products
@app.route('/')
def galleryPage():
    technologies = get_products()  # Fetching all products from the database
    return render_template('index.html', technologies=technologies)  # Rendering the homepage template with products

# Route to add items to the shopping basket
@app.route('/add_to_basket/<int:techId>')
def add_to_basket(techId):
    technology = get_product_by_id(techId)  # Fetching product details
    if not technology:
        return "Product not found", 404  # Returning a 404 error if product not found

    if 'basket' not in session:
        session['basket'] = []  # Initializing basket if it doesn't exist

    session['basket'].append(techId)  # Adding product ID to session
    session.modified = True  # Marking session as modified to save changes
    return redirect(url_for('galleryPage'))  # Redirecting to the basket page

# Route to view the shopping basket
@app.route('/basket')
def basketPage():
    if 'basket' not in session or len(session['basket']) == 0:
        return render_template('basket.html', basket_items=[], empty=True, itemTotal = 0.00, environmentScore = 0)  # Rendering empty basket page

    basket_items = [get_product_by_id(techId) for techId in session['basket']]  # Fetching product details for items in basket
    
    # basket_items is a list of items (each with .name, .price, etc.)
    item_counts = Counter([item['name'] for item in basket_items])
    
    # Deduplicate list of items by name (or use item.id if available)
    unique_items = {item['name']: item for item in basket_items}.values()
    itemTotal = round(sum(float(item['price'][1:]) for item in basket_items), 2)
    environmentScoreTotal = sum(item['environmentScore'] for item in basket_items)
    return render_template('basket.html', basket_items=basket_items, empty=False, itemTotal = itemTotal, environmentScore = environmentScoreTotal, item_counts = item_counts, unique_items = unique_items)  # Rendering basket page with items

# Route to remove items from the baske
@app.route('/remove_from_basket/<int:techId>')
def remove_from_basket(techId):
    if 'basket' in session and techId in session['basket']:
        session['basket'].remove(techId)  # Removing product from basket
        session.modified = True  # Marking session as modified to save changes
    return redirect(url_for('basketPage'))  # Redirecting to the basket page


@app.route('/individualProduct/<int:techId>')
def individualProductPage(techId):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id=?', (techId,))
    row = cursor.fetchone()
    conn.close()

    technology = {
    'id': row[0],
    'name': row[1],
    'price': row[2],
    'description': row[3],
    'image': row[4],
    'environmentScore': row[5]  
    }

    return render_template('individualProduct.html', technology = row)


@app.route('/paymentPage')
def paymentPageFunction():
    return render_template('paymentPage.html')

pattern = re.compile(r'^[A-Za-z]{1,2}\d{1,2}[A-Za-z]?\s?\d[A-Za-z]{2}$')
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    name = request.form.get("name_on_card", "")
    card_number = request.form.get("card_number", "").replace(" ", "").replace("-", "")
    expiry = request.form.get("expiry", "")
    cvv = request.form.get("cvv", "")
    postcode = request.form.get("postcode", "")
    country = request.form.get("country", "")
    city = request.form.get("city", "")
    number = request.form.get("houseFlat_number", "")

    # Basic validation
    errors = []

    if not card_number.isdigit() or len(card_number) != 16:
        errors.append("Card number must be 16 digits.")

    if not cvv.isdigit() or len(cvv) != 3:
        errors.append("CVV must be 3 digits.")

    if not name and not expiry and not postcode and not country and not city and not number:
        errors.append("All fields must be filled.")
   
    expiryDate = checkExpiryDate(expiry)
    if expiryDate == False:
        errors.append("Error with expiry date (MM/YY)")

    if not pattern.match(postcode):
        errors.append("Postcode is incorrect")

    if not number.isdigit() or int(number) < 0:
        errors.append("House/flat number is incorrect")

    if errors:
        for error in errors:
            flash(error)
        return render_template('paymentPage.html',  name_on_card=name,
                card_number=card_number,
                expiry=expiry,
                cvv=cvv,
                postcode=postcode,
                country=country,
                city=city,
                houseFlat_number=number )

    return render_template('paymentAcceptedPage.html')


def checkExpiryDate(expiry):
    try:
        # Check format MM/YY
        if '/' not in expiry:
            return False
        
        parts = expiry.split('/')
        if len(parts) != 2:
            return False

        mm, yy = parts

        # Convert to int
        mm = int(mm)
        yy = int(yy)

        # Get current month/year
        now = datetime.now()
        current_year = now.year % 100  # Get last 2 digits of year
        current_month = now.month

        # Year range check
        if yy < current_year or yy > (current_year + 10):
            return False

        # Month range check
        if mm < 1 or mm > 12:
            return False

        # If same year, month should be current or future
        if yy == current_year and mm < current_month:
            return False

        return True
    except ValueError:
        return False

@app.route('/search')
def search():
    query = request.args.get('q', '')
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE name LIKE ? OR short_description LIKE ?", 
                   ('%' + query + '%', '%' + query + '%'))
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=items, search_query=query)




# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Running the app in debug mode for development