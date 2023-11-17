from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager



#Internal imports
from .blueprints.site.routes import site
from .blueprints.authentication.routes import authentication
from .blueprints.api.routes import api
from config import Config
from .models import login_manager, db 
from .helpers import JSONEncoder

#instantiating our Flask app
app = Flask(__name__) #passing in the __name__ cariable which just takes the name of the folder we're in
app.config.from_object(Config)
jwt = JWTManager(app) #allows our app to use JWTManager from anywhere (added security for our api features)


#Wrap our app in login_manager so we can use it whenever is our app
login_manager.init_app(app)
login_manager.login_view = "authentication.sign_in"
login_manager.login_message = "Hey you Hooligan, Log in!"
login_manager.login_message_category = 'warning'



#we are going to use a decorator to create our first route
# @app.route("/")
# def hello_world():
#     return "<p>Hello You Hooligan!</p>"

app.register_blueprint(site)
app.register_blueprint(authentication)
app.register_blueprint(api)

#instantiating our database & wrapping our app
db.init_app(app)
migrate = Migrate(app,db)
app.json_encoder = JSONEncoder #no parentheses because we are not instantiating an object we are simple pointing to this class we made when we need to encode data objects
cors = CORS(app) #Cross Origin Resource Sharing aka allowing other apps to talk to our flask app/server