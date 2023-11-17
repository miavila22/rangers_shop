#this is our configuration folder to configure flask to our app location
#& variables needed to run Flask

from datetime import timedelta
import os #just importing operating system
from dotenv import load_dotenv #allows us to load our environment variables(need to run app)

#establish base directory so whenever we use "." to reference any location in our app it knows we are referencing
#rangers_shop folder
basedir = os.path.abspath(os.path.dirname(__file__))

#need to establish where our environment variables are coming from 
# (this file will be hidden on the github)
load_dotenv(os.path.join(basedir, '.env'))

#------------create our config Class
class Config():

    """
    Create Config class which will setup our configuration variables.
    Using Environment variables where available other create config variables.
    """
    #regular configuration for Flask App
    FLASK_APP = os.environ.get('FLASK_APP') #looking for key of FLASK_APP in our environment variable location (.env)
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')

    #configuration if you are connecting a database
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Literally whatever you want as long as its a string. Cool beans'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False #We dont want a message every single time our database is changed.
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES =timedelta(days=365) 