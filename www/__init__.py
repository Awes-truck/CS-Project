from flask import Flask
import pymysql


def sql_connect(host, port, user, password, database):
    connect = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    return connect


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'sgeswgw43twsfwq3fafsdfq3'
    # will be set dependent on where the app is hosted
    app.config['SQL_HOST'] = ''
    app.config['SQL_PORT'] = 0
    app.config['SQL_USER'] = ''
    app.config['SQL_PASSWORD'] = ''
    app.config['SQL_DATABASE'] = ''

    from.views import views
    from.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
