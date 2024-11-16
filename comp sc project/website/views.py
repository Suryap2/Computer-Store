from flask import Blueprint, render_template

views=Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

# @views.route('/products')
# def products():
#     return render_template('products.html')

# @views.route('/checkout')
# def checkout():
#     return render_template('checkout.html')

