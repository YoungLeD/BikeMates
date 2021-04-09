from flask import Flask

from app.config import get_config
from app.extensions import *
import os

# Flask
app = Flask(__name__)

# Config
config(app, get_config())

# DB
db_config = get_config()['database']

# Files
UPLOAD_FOLDER = os.path.join('app', 'static', 'avatar', '')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

connect_string = 'postgresql+pypostgresql://{}:{}@{}:{}/{}'.format(
    db_config['user'], db_config['password'], db_config['host'],
    db_config['port'], db_config['dbname'])
app.config['SQLALCHEMY_DATABASE_URI'] = connect_string
db = SQLAlchemy(app)

# API
from app.api import v1_0

# Site
from app import views
