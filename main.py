from www import create_app
#import mysql.connector
import pymysql

app = create_app()

app.config['SECRET_KEY'] = 'sgeswgw43twsfwq3fafsdfq3'
host = '86.173.55.216'
port = 3306
user = 'root'
password = ''


if __name__ == '__main__':
    app.run(debug=True)
