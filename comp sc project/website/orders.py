from flask import Blueprint, render_template, session
from flask_mysqldb import MySQL

mysql = MySQL()
orders = Blueprint('orders', __name__)

@orders.route('/orders')
def show_orders():
    # Get the current user id from session
    user_id = session['user']['id']

    # Fetch the orders of the user
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT o.id, o.total_price, o.order_date , o.address, o.payment_info
        FROM orders o 
        WHERE o.user_id = %s
    ''', (user_id,))
    user_orders = cursor.fetchall()

    # Create a list to store orders with their items
    orders_with_items = []

    # Loop through each order and fetch its items
    for order in user_orders:
        order_id, total_price, order_date,address,payment_info = order
        cursor.execute('''
            SELECT oi.pname, oi.price, oi.quantity 
            FROM order_items oi 
            WHERE oi.order_id = %s
        ''', (order_id,))
        order_items = cursor.fetchall()

        if payment_info:
            if '@' in payment_info:
                payment_info = 'UPI'
            elif 'Cash' in payment_info:
                payment_info = 'Cash on Delivery'
            else:
                payment_info = 'Card'

        # Append order and its items to the list
        orders_with_items.append({
            'order_id': order_id,
            'total_price': total_price,
            'order_date': order_date,
            'address' : address,
            'payment_info' : payment_info,
            'items': order_items
        })

    cursor.close()

    # Render the orders template and pass the orders with items
    return render_template('orders.html', orders_with_items=orders_with_items)