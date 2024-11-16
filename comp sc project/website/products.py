from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
import base64

mysql = MySQL()

products=Blueprint('products',__name__)

@products.route('/products')
def getProducts():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, name, description, price,image FROM products')
    products = cursor.fetchall()
    cursor.close()

    products = [list(product) for product in products]

    for product in products:
        image_b64 = base64.b64encode(product[4]).decode('utf-8')
        product[4] = image_b64

    return render_template('products.html', products=products)

@products.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    
    # Fetch product details from the database
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT name, price,image,description FROM products WHERE id = %s', (product_id,))
    product = cursor.fetchone()
    pname, unit_price = product[0], product[1]
    
    if 'cartProducts' not in session:
        session['cartProducts'] = {}
        
    if product_id in session['cartProducts']:
        session['cartProducts'][product_id] += 1  # Increment the count if the product is already in the cart
    else:
        session['cartProducts'][product_id] = 1  # Add the product with a count of 1

    # Total number of that product in the cart
    tno = session['cartProducts'][product_id]
    
    # Calculate total price based on quantity
    total_price = unit_price * tno

    # Insert or update the product in the cart table
    cursor.execute('''
        INSERT INTO cart (pname, price, tno,image,description)
        VALUES (%s, %s, %s,%s,%s)
        ON DUPLICATE KEY UPDATE
            tno = VALUES(tno), 
            price = price + VALUES(price)
    ''', (pname, unit_price, tno,product[2],product[3]))

    mysql.connection.commit()
    cursor.close()

    session.modified = True    
    flash('Successfully added to Cart!', category='success')
    print("Cart products : ", session['cartProducts'])

    return redirect(url_for('products.getProducts'))

@products.route('/search', methods=['POST'])
def search_products():
    search_query = request.form.get('search_query')
    
    # Fetch products from the database based on the search keyword
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT id, name, description, price, image 
        FROM products 
        WHERE name LIKE %s OR description LIKE %s
    ''', ('%' + search_query + '%', '%' + search_query + '%'))
    
    matching_products = cursor.fetchall()
    cursor.close()
    
    # Convert the results into a list to prepare for rendering
    products_list = [list(product) for product in matching_products]
    
    # Convert the image data to base64 if you are storing images in the DB
    for product in products_list:
        image_b64 = base64.b64encode(product[4]).decode('utf-8')
        product[4] = image_b64
    
    return render_template('products.html', products=products_list, search_query=search_query)






