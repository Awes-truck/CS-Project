from www import create_app, sql_connect
import pymysql
from flask import request
from urllib.parse import urlparse

app = create_app()


@app.before_first_request
def before_first_request_func():
    global LOCAL_SQL_MODE
    url = urlparse(request.base_url)
    hostname = url.hostname
    print("Connected to %s" % hostname)
    if hostname == "localhost":
        app.config['SQL_HOST'] = 'localhost'
        app.config['SQL_PORT'] = 3306
        app.config['SQL_USER'] = 'root'
        connect = sql_connect(
            app.config['SQL_HOST'],
            app.config['SQL_PORT'],
            app.config['SQL_USER'],
            app.config['SQL_PASSWORD'],
            app.config['SQL_DATABASE']
        )

        cursor = connect.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS wgccc")
        connect.commit()
        connect.close()

        app.config['SQL_DATABASE'] = 'wgccc'
        connect = sql_connect(
            app.config['SQL_HOST'],
            app.config['SQL_PORT'],
            app.config['SQL_USER'],
            app.config['SQL_PASSWORD'],
            app.config['SQL_DATABASE']
        )

        cursor = connect.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users
            (id INT(6) PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(255),
            family_name VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255),
            address VARCHAR(255))''')
        connect.commit()
        connect.close()


if __name__ == '__main__':
    app.run(debug=True)
