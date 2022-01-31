from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app as app
from datetime import datetime
# import pymysql
from .__init__ import sql_connect
# from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.get('email')
        password = request.get('password')

    return render_template("login.html",  datetime=str(datetime.now().year))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    postal_keys = [
        'street_number',
        'route',
        'postal_town',
        'administrative_area_level_2',
        'postal_code'
    ]
    full_address_list = []
    separator = ', '

    if request.method == 'POST':
        email = str(request.form.get('email'))
        first_name = request.form.get('first_name')
        family_name = request.form.get('family_name')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        for i in postal_keys:
            full_address_list.append(str(request.form.get(i)))
            print(str(request.form.get(i)))
        full_address = separator.join(full_address_list)
        print(full_address)

        if len(email) < 4:
            flash('Email must be greater 3 characters', category='error')
        elif len(first_name) < 4:
            flash('First Name must be greater than 3 characters', category='error')
        elif len(family_name) < 4:
            flash('Family Name must be greater than 3 characters', category='error')
        elif password != password_confirm:
            flash('Passwords do not match', category='error')
        elif len(password) < 8:
            flash('Password must be greater than 7 characters', category='error')
        else:
            # for i in user_detail_keys:
            #     new_user = separator.join(i)
            connect = sql_connect(
                app.config['SQL_HOST'],
                app.config['SQL_PORT'],
                app.config['SQL_USER'],
                app.config['SQL_PASSWORD'],
                app.config['SQL_DATABASE']
            )
            cursor = connect.cursor()
            cursor.execute(
                '''INSERT INTO users (first_name, family_name, email) VALUES ('%s', '%s', '%s')'''
                % (first_name, family_name, email))
            connect.commit()
            connect.close()
            flash('Account successfully created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("register.html",  datetime=str(datetime.now().year))
