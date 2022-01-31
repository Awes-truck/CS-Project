from www import create_app
# import mysql.connector
import pymysql
from flask import request
from urllib.parse import urlparse

app = create_app()
app.config['SECRET_KEY'] = 'sgeswgw43twsfwq3fafsdfq3'
LOCAL_SQL_MODE = False


@app.before_first_request
def before_first_request_func():
    global LOCAL_SQL_MODE
    url = urlparse(request.base_url)
    hostname = url.hostname
    print("Connected to %s" % hostname)
    if hostname == "localhost":
        sql_host = hostname
        sql_port = 3306
        sql_user = 'root'
        sql_password = ''

        connect = pymysql.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
        )

        cursor = connect.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS wgccc")
        connect.commit()
        connect.close()

        new_db = pymysql.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database='wgccc'
        )

        cursor = new_db.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users
            (id INT(6) PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(255),
            family_name VARCHAR(255),
            email VARCHAR(255))''')
        new_db.commit()
        new_db.close()


if __name__ == '__main__':
    app.run(debug=True)
