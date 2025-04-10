from flask import Flask, render_template, request, redirect, url_for, session  # Importing necessary Flask modules
from flask_wtf import FlaskForm  # Importing Flask-WTF for form handling
from wtforms import StringField, SubmitField  # Importing form fields from WTForms
from wtforms.validators import DataRequired, Length  # Importing validators for form validation
from flask_bootstrap import Bootstrap  # Importing Bootstrap for styling
import sqlite3  # Importing SQLite for database operations

app = Flask(__name__)  # Creating a Flask web application instance
bootstrap = Bootstrap(app)  # Initializing Flask-Bootstrap for UI styling
app.config['SECRET_KEY'] = "top secret password don't tell anyone this"  # Setting a secret key for session security

# Function to fetch all products from the SQLite database
def get_products():
    conn = sqlite3.connect('products.db')  # Connecting to the database
    cursor = conn.cursor()  # Creating a cursor object to execute SQL queries
    cursor.execute("SELECT id, name, price, description, image FROM products")  # Querying all products
    
    # Fetching all results and formatting them as dictionaries
    products = [
        {"id": row[0], "name": row[1], "price": row[2], "description": row[3], "image": row[4]}
        for row in cursor.fetchall()
    ]
    conn.close()  # Closing the database connection
    return products  # Returning the list of products

# Function to fetch a single product by ID
def get_product_by_id(tech_id):
    conn = sqlite3.connect('products.db')  # Connecting to the database
    cursor = conn.cursor()  # Creating a cursor object
    cursor.execute("SELECT id, name, price, description, image FROM products WHERE id = ?", (tech_id,))  # Querying a specific product
    row = cursor.fetchone()  # Fetching the result
    conn.close()  # Closing the connection
    
    # If a product exists, return it as a dictionary
    if row:
        return {"id": row[0], "name": row[1], "price": row[2], "description": row[3], "image": row[4]}
    return None  # Return None if product not found


# Route for the homepage displaying all products
@app.route('/')
def galleryPage():
    technologies = get_products()  # Fetching all products from the database
    return render_template('index.html', technologies=technologies)  # Rendering the homepage template with products


# Route for displaying a single product
#def singleProductPage(techId):
#    techId += 1  # Incrementing the ID (possible bug as IDs start from 1)
#    technology = get_product_by_id(techId)  # Fetching product details
#    if not technology:
#        return "Product not found", 404  # Returning a 404 error if product not found

#    form = OpinionForm()  # Creating an instance of the form
#    if form.validate_on_submit():  # Checking if the form is submitted and valid
#        quantity = form.quantity.data  # Getting the user input
#        return render_template('SingleTechOpinion.html', technology=technology, product=technology["name"], quantity=quantity)  # Rendering opinion page

#    return render_template('SingleTech.html', technology=technology, form=form)  # Rendering product page with form


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
    return redirect(url_for('basketPage'))  # Redirecting to the basket page

# Route to view the shopping basket
@app.route('/basket')
def basketPage():
    if 'basket' not in session or len(session['basket']) == 0:
        return render_template('basket.html', basket_items=[], empty=True)  # Rendering empty basket page

    basket_items = [get_product_by_id(techId) for techId in session['basket']]  # Fetching product details for items in basket
    return render_template('basket.html', basket_items=basket_items, empty=False)  # Rendering basket page with items

# Route to remove items from the basket
@app.route('/remove_from_basket/<int:techId>')
def remove_from_basket(techId):
    if 'basket' in session and techId in session['basket']:
        session['basket'].remove(techId)  # Removing product from basket
        session.modified = True  # Marking session as modified to save changes
    return redirect(url_for('basketPage'))  # Redirecting to the basket page

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Running the app in debug mode for development