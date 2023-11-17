#External imports
from werkzeug.security import generate_password_hash #generates a unique password hash for extra security
from flask_sqlalchemy import SQLAlchemy #this is our ORM (Object Relational Mapper)
from flask_login import UserMixin, LoginManager #helping us load a user as our current_user
from datetime import datetime #allow us to put a timestamp on any data we create
import uuid #makes a unique id for our data. (primary key)
from flask_marshmallow import Marshmallow

#internal imports
from .helpers import get_image


#instantiate all our classes
db = SQLAlchemy() # make database object
login_manager = LoginManager() # make login object
ma = Marshmallow()


#use login_manager object to create a user_loader function
@login_manager.user_loader
def load_user(user_id):
    """
    Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id) #this is basic query inside our database to bring back a specific User Object

#Think of these as admin. (keeping track of what prodcuts are available to sell like a Warehouse.)
class User(db.Model, UserMixin):
    #CREATE TABLE USER, all the columns we create
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


    #INSERT INTO User() Values()

    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email 
        self.password = self.set_password(password)

    #METHODS for editing our attributes
    def set_id(self):
        return str(uuid.uuid4()) #all this is doing is creating a unique identification token 
    

    def get_id(self):
        return str(self.user_id) #UserMixin using this method to grab the user_id on the object logged in
    
    def set_password(self, password):
        return generate_password_hash(password)#hashes the password so it is secure (basically, no one can see it)
    
    def __repr__(self):
        return f"<User: {self.username}>"
    

class Product(db.Model): #helps us translate python code to columns in SQL
    prod_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String)
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #eventually we need to connect this to orders. 

    def __init__(self, name, price, quantity, image="", description=""):
        self.prod_id = self.set_id()
        self.name = name
        self.image = self.set_image(image, name)
        self.description = description
        self.price = price
        self.quantity = quantity

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_image(self, image, name):
        if not image: #the user did not give us an image
            image = get_image(name)# name is going to become search and we are going to use it to make our API call
            #come back and add our api call
        return image
    
    #we need a method for when customers buy products to decrement and increment our quantity

    def decrement_quantity(self, quantity):

        self.quantity -= int(quantity)
        return self.quantity 
    
    def increment_quantity(self, quantity):

        self.quantity += int(quantity)
        return self.quantity

    def __repr__(self):
        return f"<Product: {self.name}>"
    

#only need this for purposes of tracking what customers are tied to what orders and also how many customers we have
class Customer(db.Model):
    cust_id = db.Column(db.String, primary_key=True)
    date_created = db.Column(db.String, default = datetime.utcnow())
    #this is how we tie a table to another one. NOT A COLUMN just establising a relationship
    prodord = db.relationship('ProdOrder', backref = 'customer', lazy=True) #lazy=True means is we don't need the ProdOrder table to have a customer

    def __init__(self, cust_id):
        self.cust_id = cust_id #when a customer makes an order on the frontend, they will pass us their cust_id

    def __repr__(self):
        return f"<Customer: {self.cust_id}>"
    

#example of a join table because Products can be on many Orders and Orders can have many Products 
# (many-many) relationship needs a Join Table

class ProdOrder(db.Model):
    prodorder_id = db.Column(db.String, primary_key=True)
    #first instance of using a primary key as a foreign key on this table
    prod_id = db.Column(db.String, db.ForeignKey('product.prod_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    order_id = db.Column(db.String, db.ForeignKey('order.order_id'), nullable=False)
    cust_id = db.Column(db.String, db.ForeignKey('customer.cust_id'), nullable=False)

    def __init__(self, prod_id, quantity, price, order_id, cust_id):
        self.prodorder_id = self.set_id()
        self.prod_id = prod_id
        self.quantity = quantity
        self.price = self.set_price(quantity, price)
        self.order_id = order_id
        self.cust_id = cust_id

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_price(self, quantity, price):
        quantity = int(quantity)
        price = float(price)

        self.price = quantity * price #this is the total price for that product multiplied by quantity purchased
        return self.price

    def update_quantity(self, quantity):
        self.quantity = int(quantity)
        return self.quantity

class Order(db.Model):
    order_id = db.Column(db.String, primary_key=True)
    order_total = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    prodord = db.relationship('ProdOrder', backref = 'order', lazy=True)#establishing a relationship, NOT A COLUMN 
    

    def __init__(self):
        self.order_id = self.set_id()
        self.order_total = 0.00
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def increment_ordertotal(self, price):
        self.order_total = float(self.order_total)
        self.order_total += float(price)

        return self.order_total
    
    def decrement_ordertotal(self, price):
        self.order_total = float(self.order_total)
        self.order_total -= float(price)

        return self.order_total
    
    def __repr__(self):
        return f"<Order: {self.order_id}>"


    

#creating our schema class (Schema essentially just means what our data "looks" like,
# and our data needs to look like a dictionary (json) not an object)

class ProductSchema(ma.Schema):

    class Meta:
        fields = ['prod_id', 'name', 'image', 'description', 'price', 'quantity']

#instantiate our ProductSchema class so we can use them in our application
product_schema = ProductSchema() #this is 1 singular product ONLY ONE
products_schema = ProductSchema(many=True) #bringing back all of the products in our database and sending to frontend


