from flask import Blueprint, flash, redirect, render_template, request, session, url_for, Response
from flask_mysqldb import MySQL
import base64
import csv
from io import StringIO

mysql = MySQL()

manage=Blueprint('manage',__name__)

@manage.route('/manage')
def show_manage():
    # Fetch all products from the database to display in the manage view
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, name, description, price, image FROM products')
    products = cursor.fetchall()
    cursor.close()

    # Convert image data to base64 for display, if needed
    products = [
        {
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],
            'image': base64.b64encode(product[4]).decode('utf-8')
        }
        for product in products
    ]

    return render_template('manage.html', products=products)

@manage.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    cursor = mysql.connection.cursor()

    try:
        # Execute delete query to remove the product by id
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        mysql.connection.commit()  # Commit the transaction to save changes

        flash("Product deleted successfully!", "success")
    except Exception as e:
        mysql.connection.rollback()  # Roll back if there's any error
        flash("An error occurred while trying to delete the product.", "danger")
        print(f"Error deleting product: {e}")
    finally:
        cursor.close()

    # Redirect back to the manage page to see the updated product list
    return redirect(url_for('manage.show_manage'))

# In manage.py

@manage.route('/add_or_edit_product', methods=['POST'])
def add_or_edit_product():
    product_id = request.form.get('product_id')
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    image = request.files.get('image')

    cursor = mysql.connection.cursor()

    image_file_path = 'C:/Users/gagan/OneDrive/Desktop/Surya/12D stuff/comp sc project/website/images.bin'
    
    if product_id:  # Edit product
        query = "UPDATE products SET name = %s, description = %s, price = %s WHERE id = %s"
        params = (name, description, price, product_id)
        
        # If a new image was uploaded, update it
        if image:
            image_data = image.read()
            query = "UPDATE products SET name = %s, description = %s, price = %s, image = %s WHERE id = %s"
            params = (name, description, price, image_data, product_id)
            
        flash("Product updated successfully!", "success")
    else:  # Add new product
        if image:
            image_data = image.read()
            query = "INSERT INTO products (name, description, price, image) VALUES (%s, %s, %s, %s)"
            params = (name, description, price, image_data)

            # Append the new image to the binary file
            with open(image_file_path, 'ab') as file:
                file.write(image_data)

            flash("Product added successfully!", "success")
        else:
            flash("Image is required to add a new product.", "danger")
            return redirect(url_for('manage.show_manage'))

    cursor.execute(query, params)
    mysql.connection.commit()
    cursor.close()
    
    return redirect(url_for('manage.show_manage'))

@manage.route('/export_products')
def export_products():
    # Query to fetch all products from the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id,name, description, price FROM products")
    products = cursor.fetchall()
    cursor.close()
    
    # Create an in-memory CSV file
    si = StringIO()
    csv_writer = csv.writer(si)
    
    # Write headers
    csv_writer.writerow(['Product ID','Product Name', 'Description', 'Price'])
    
    # Write product data
    for product in products:
        csv_writer.writerow(product)
    
    # Prepare CSV file response
    output = si.getvalue()
    response = Response(output, mimetype='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=products.csv"
    return response
