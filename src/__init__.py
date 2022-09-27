from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///khmerasr.db'
app.config['SECRET_KEY'] = 'ef4c1adcbabd874ea94f6908'
app.config['UPLOAD_FOLDER'] = 'static/storage/audios/samples'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "signin_page"
# login_manager.login_message_category = 'info'
login_manager.login_message = "Please sign in to continue"

GOGOLE_CLIENT_ID = "290046354585-8b9n0ch4m25tq9ebtblffkgs23q9vp5p.apps.googleusercontent.com"

from src.routes import routes