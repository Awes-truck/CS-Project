from www import create_app
#import mysql.connector
import pymysql

app = create_app()

app.config['SECRET_KEY'] = 'sgeswgw43twsfwq3fafsdfq3'
host = 'fdb33.awardspace.net'
port = 3306
user = '4031935_wgcc'
password = ''

connect = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
)


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


setup_database()

if __name__ == '__main__':
    app.run(debug=True)
