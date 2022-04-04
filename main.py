from www import create_app, sql_connect
from flask import request
from urllib.parse import urlparse
from datetime import timedelta
import os

# Create a new application
app = create_app()

# Set Session persistence to a specified amount of days
app.permanent_session_lifetime = timedelta(days=7)

'''
Before the first request is sent to the application, we want to make sure
the database is up to date and automatically create and populate if not
'''


@app.before_first_request
def before_first_request_func():
    # DEVELOPMENT PURPOSES
    url = urlparse(request.base_url)
    hostname = url.hostname
    print("Connected to %s" % hostname)

    SQL_HOST = os.getenv("SQL_HOST")
    SQL_PORT = int(os.getenv("SQL_PORT"))
    SQL_USER = os.getenv("SQL_USER")
    SQL_PASSWORD = os.getenv("SQL_PASSWORD")
    SQL_DATABASE = ''

    # Database connection
    connect = sql_connect(
        SQL_HOST,
        SQL_PORT,
        SQL_USER,
        SQL_PASSWORD,
        SQL_DATABASE
    )

    # Create a new database instance
    cursor = connect.cursor()
    # Create the database if it doesn't exist
    cursor.execute('CREATE DATABASE IF NOT EXISTS awestruck')
    # Save changes
    connect.commit()
    cursor.close()

    # Now we can grab the database we just created
    connect.select_db(os.getenv("SQL_DATABASE"))

    cursor = connect.cursor()
    # Create usergroups table if it doesnt already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usergroups(
            group_id INT(6) PRIMARY KEY AUTO_INCREMENT,
            description VARCHAR(255) NOT NULL,
            price_id VARCHAR(100)
        );
    ''')
    cursor.close()
    cursor = connect.cursor()
    # Create Seniors table if it doesnt already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seniors(
            senior_id INT(6) PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(40) NOT NULL,
            family_name VARCHAR(40) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            address VARCHAR(255) NOT NULL,
            phone_number VARCHAR(30),
            group_id INT(6),
            FOREIGN KEY (group_id) REFERENCES usergroups(group_id)
        );
    ''')
    cursor.close()
    cursor = connect.cursor()
    # Create Juniors table if it doesnt already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS juniors(
            junior_id INT(6) PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(40) NOT NULL,
            family_name VARCHAR(40) NOT NULL,
            dob DATE NOT NULL,
            senior_id INT(6),
            FOREIGN KEY (senior_id) REFERENCES seniors(senior_id),
            is_developmental BIT(1) DEFAULT 0
        );
    ''')
    cursor.close()
    cursor = connect.cursor()
    # Populate the usergroups table if the information isn't there
    cursor.execute('''
        INSERT IGNORE INTO usergroups
            (group_id, description, price_id)
        VALUES
            (1, 'Administrator', NULL),
            (2, 'General User', NULL),
            (3, 'Social Member', 'price_1KTT07HuaTKPzffSkYKw4EPw'),
            (4, 'Senior Member', 'price_1KTNDVHuaTKPzffS1ubgGAr7'),
            (5, 'Senior Member in Full Time Education or Unemployed', 'price_1KTS4HHuaTKPzffSsYTpJcNQ')
    ''')
    connect.commit()
    cursor.close()


# Run our app
if __name__ == '__main__':
    app.run(debug=True)
