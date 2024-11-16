from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
import base64

mysql = MySQL()

checkout = Blueprint('checkout', __name__)

@checkout.route('/checkout', methods=['GET', 'POST'])
def show_checkout():
    if request.method == 'POST':
        # Get user details from session
        user_id = session['user']['id']
        if not user_id:
            flash('You must be logged in to place an order', 'error')
            return redirect(url_for('auth.login'))
        
        # Get form data
        address = request.form.get('address')
        payment_method = request.form.get('paymentMethod')

        print(address,payment_method)

        # Determine the payment information based on the selected method
        if payment_method == 'card':
            payment_info = request.form.get('Card')
        elif payment_method == 'upi':
            payment_info = request.form.get('UPI')
        elif payment_method == 'cod':
            payment_info = "Cash on Delivery"
        else:
            flash('Invalid payment method', 'error')
            return redirect(url_for('checkout.show_checkout'))

        # Query the cart table to get the products
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT pname, price, tno FROM cart')
        cart_products = cursor.fetchall()

        # Calculate total price
        cart_total = sum([product[1] * product[2] for product in cart_products])

        # Insert a new order in the orders table
        cursor.execute('''
            INSERT INTO orders (user_id, total_price,address,payment_info) 
            VALUES (%s, %s,%s,%s)
        ''', (user_id, cart_total,address,payment_info))
        order_id = cursor.lastrowid  # Get the ID of the newly created order

        # Insert each cart item into the order_items table
        for product in cart_products:
            pname, price, tno = product
            cursor.execute('''
                INSERT INTO order_items (order_id, pname, price, quantity)
                VALUES (%s, %s, %s, %s)
            ''', (order_id, pname, price, tno))

        # Clear the cart after order is placed
        cursor.execute('DELETE FROM cart')
        session.pop('cartProducts', None)
        mysql.connection.commit()
        cursor.close()

        flash('Order placed successfully!', 'success')
        return render_template('home.html')

    else:
        # GET request, render the checkout page
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT pname, price, tno, image,description FROM cart')
        cart_products = cursor.fetchall()

        cart_products = [list(product) for product in cart_products]
        cart_total = sum([product[1] for product in cart_products])

        for product in cart_products:
            image_b64 = base64.b64encode(product[3]).decode('utf-8')
            product[3] = image_b64

        cursor.close()

        return render_template('checkout.html', cart_products=cart_products, cart_total=cart_total)
    
@checkout.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_name = request.form.get('product_name')

    # Remove the product from the cart table
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM cart WHERE pname = %s', (product_name,))
    mysql.connection.commit()

    # Remove the product from the session cart
    if 'cartProducts' in session and product_name in session['cartProducts']:
        del session['cartProducts'][product_name]
        session.modified = True

    # Recalculate total after deletion
    cursor.execute('SELECT SUM(price * tno) FROM cart')
    updated_total = cursor.fetchone()[0] or 0

    cursor.close()
    flash(f'{product_name} removed from cart.', 'success')

    # Redirect to show_checkout to refresh the cart with updated data
    return redirect(url_for('checkout.show_checkout'))