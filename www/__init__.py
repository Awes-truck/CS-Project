from flask import Flask
import pymysql
from dotenv import load_dotenv
import os

project_folder = os.path.expanduser('www')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))


# SQL Connection Function


def sql_connect(host, port, user, password, database):
    connect = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    return connect

# Create the Flask Applcation


def create_app():
    app = Flask(__name__)
    # The app needs a secret key to work, grab it from the .env file
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    # Create our page blueprints
    from.views import views
    from.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
