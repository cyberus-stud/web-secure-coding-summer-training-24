from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a04278a3fd177533fb3ab02b0cd0cfd6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) # this will manage all the sessions in the background for us after adding some functionalty in the database models
login_manager.login_view = 'login' # this tells extention where our login route is located & 'login' like the url for function 
login_manager.login_message_category = 'info' # blue information alert

from flaskshop import routes