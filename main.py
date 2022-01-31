from www import create_app
# import mysql.connector
import pymysql
import socket

app = create_app()
app.config['SECRET_KEY'] = 'sgeswgw43twsfwq3fafsdfq3'
LOCAL_SQL_MODE = False

if socket.gethostbyname("localhost"):
    print("Localhosting enabled!")
    LOCAL_SQL_MODE = True


def setup_database():
    cursor = connect.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS wgccc")
    connect.commit()
    connect.close()

    new_db = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
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


if LOCAL_SQL_MODE is True:
    host = 'localhost'
    port = 3306
    user = 'root'
    password = ''

    connect = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
    )

    setup_database()


if __name__ == '__main__':
    app.run(debug=True)
