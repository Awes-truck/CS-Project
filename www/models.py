from . import mysql
from flask_login import UserMixin


class User(mysql.Model, UserMixin):
    id = mysql.Column(mysql.Integer, primary_key=True)
    email = mysql.Column(mysql.String(150), unique=True)
    password = mysql.Column(db.String)
