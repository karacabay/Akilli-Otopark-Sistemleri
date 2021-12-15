from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///otopark.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from AkilliOtopark import routes

 