from www import create_app
from flask_mysqldb import MySQL

app = create_app()

app.config['SECRET_KEY'] = 'sgeswgw43twsfwq3fafsdfq3'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'wgccc'

mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)
