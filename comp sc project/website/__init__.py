from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

#creating flask app
def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='hahah'

    # MySQL configurations
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'gagan123'
    app.config['MYSQL_DB'] = 'quantum_bytes'

    mysql.init_app(app)

    from .views import views
    from .auth import auth
    from .products import products
    from .checkout import checkout
    from .orders import orders
    from .manage import manage


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(products,url_prefix='/')
    app.register_blueprint(checkout,url_prefix='/')
    app.register_blueprint(orders,url_prefix='/')
    app.register_blueprint(manage,url_prefix='/')
    return app


