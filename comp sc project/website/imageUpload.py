from flask_mysqldb import MySQL
mysql = MySQL()

# Open a connection to your database
db = mysql.connect("localhost", "root", "gagan123", "quantum_bytes")
cursor = db.cursor()

# Open the image file in binary mode
with open("KeyBoard.png", 'rb') as file:
    image_data = file.read()

# SQL query to insert the image along with product details
sql = """INSERT INTO products (image) 
         VALUES (%s)"""
cursor.execute(sql, (image_data))

# Commit the changes
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()
