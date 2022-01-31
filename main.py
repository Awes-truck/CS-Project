from www import create_app
import pymysql
from flask import request
from urllib.parse import urlparse

app = create_app()
app.config['SECRET_KEY'] = 'sgeswgw43twsfwq3fafsdfq3'
LOCAL_SQL_MODE = False


def sql_connect(host, port, user, password, database):
    connect = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    return connect


@app.before_first_request
def before_first_request_func():
    global LOCAL_SQL_MODE
    url = urlparse(request.base_url)
    hostname = url.hostname
    print("Connected to %s" % hostname)
    if hostname == "localhost":
        connect = sql_connect('localhost', 3306, 'root', '', '')

        cursor = connect.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS wgccc")
        connect.commit()
        connect.close()

        connect = sql_connect('localhost', 3306, 'root', '', 'wgccc')

        cursor = connect.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users
            (id INT(6) PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(255),
            family_name VARCHAR(255),
            email VARCHAR(255))''')
        connect.commit()
        connect.close()


if __name__ == '__main__':
    app.run(debug=True)
