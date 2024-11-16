from flask import Blueprint, session, render_template, request, flash
from flask_mysqldb import MySQL

mysql = MySQL()

auth=Blueprint('auth',__name__)

#defining login logout and signup
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password1=request.form.get('password')
        
        if len(email)==0:
            flash('Enter the correct Email', category='error')
        elif len(password1) < 10:
            flash('Password must be atleast 10 characters.', category='error')
        else:
            try:
                cursor = mysql.connection.cursor()
                # Query to check if email and password match
                cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password1))
                user = cursor.fetchone()

                if user:
                    session['user'] = {
                        'id': user[0],  
                        'email': user[1],
                        'firstName': user[2],
                        'isAdmin':user[4]
                    }
                    flash('Successfully Logged in!', category='success')
                    print("user : ",session['user'])
                    return render_template('home.html' )
                else:
                    flash('Email or Password Invalid', category='error')

                cursor.close()
            except Exception as e:
                mysql.connection.rollback() 
                flash('Email or Password Invalid', category='error')

    return render_template('login.html' )

@auth.route('/logout')
def logout():
    session.clear()  # Clears the entire session, including the user object
    flash('Successfully Logged out!', category='success')
    return render_template('home.html' )

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        if len(email)==0:
            flash('Please Enter Email', category='error')
        elif len(firstName)==0:
            flash('Enter your first Name', category='error')
        elif len(password1) < 10:
            flash('Password must be atleast 10 characters.', category='error')
        elif password1 != password2:
            flash('Passwords dont Match.', category='error')
        else:
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO user (email, firstName, password) VALUES (%s, %s, %s)', (email, firstName, password1))
                mysql.connection.commit()

                user_id = cursor.lastrowid
                cursor.close()

                # Store user information in session
                session['user'] = {
                    'id': user_id,
                    'email': email,
                    'firstName': firstName,
                    'isAdmin': 0
                }

                flash('Account Created Successfully!', category='success')
                return render_template('home.html')
            except Exception as e:
                mysql.connection.rollback()  # Rollback in case of error
                flash('Error in Creation of Account!', category='error')

    return render_template('signup.html')








