from flask import Flask
import pymysql
import random
import string
from werkzeug.security import generate_password_hash as key_hash
from dotenv import load_dotenv
import os

project_folder = os.path.expanduser('www')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))


def sql_connect(host, port, user, password, database):
    connect = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    return connect


def generate_secret_key():
    chars = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(random.choice(chars) for i in range(8))
    return secret_key


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = key_hash(generate_secret_key())
    # will be set dependent on where the app is hosted

    from.views import views
    from.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
