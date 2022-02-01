from flask import Blueprint, render_template, redirect, session, url_for, request, flash, current_app as app
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
# import pymysql
from .__init__ import sql_connect
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    connect = sql_connect(
        app.config['SQL_HOST'],
        app.config['SQL_PORT'],
        app.config['SQL_USER'],
        app.config['SQL_PASSWORD'],
        app.config['SQL_DATABASE']
    )

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = connect.cursor()
        user = cursor.execute(
            '''SELECT id, password, first_name FROM users WHERE email='%s' '''
            % email
        )
        user = cursor.fetchone()
        if user:
            user_id = user[0]
            user_password_hash = user[1]
            user_name = user[2]
            if check_password_hash(user_password_hash, password):
                session.permanent = True
                session['loggedin'] = True
                session['email'] = email
                session['name'] = user_name
                flash('Logged in Successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Please try again!', category='error')
        else:
            flash('Incorrect email. Please try again!', category='error')
    return render_template("login.html",  datetime=str(datetime.now().year))


@auth.route('/logout')
def logout():
    if session['loggedin']:
        session.pop('email', None)
        session.pop('name', None)
        session.pop('loggedin', None)
    return redirect(url_for('views.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    connect = sql_connect(
        app.config['SQL_HOST'],
        app.config['SQL_PORT'],
        app.config['SQL_USER'],
        app.config['SQL_PASSWORD'],
        app.config['SQL_DATABASE']
    )
    postal_keys = [
        'street_number',
        'route',
        'postal_town',
        'administrative_area_level_2',
        'postal_code'
    ]
    full_address_list = []
    separator = ', '
    full_address_complete = True
    email_exists = False

    if request.method == 'POST':
        email = str(request.form.get('email'))
        first_name = request.form.get('first_name')
        family_name = request.form.get('family_name')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        cursor = connect.cursor()
        query = cursor.execute(
            '''SELECT email FROM users WHERE email = '%s' ''' % email)
        if query != 0:
            email_exists = True
        cursor.close()

        for i in postal_keys:
            if str(request.form.get(i)) == "":
                full_address_complete = False
                break
            else:
                full_address_list.append(str(request.form.get(i)))
        if full_address_complete:
            full_address = separator.join(full_address_list)
            print(full_address)

        if len(email) < 4:
            flash('Email must be greater 3 characters', category='error')
        elif email_exists:
            flash('Email already exists!', category='error')
        elif len(first_name) < 4:
            flash('First Name must be greater than 3 characters', category='error')
        elif len(family_name) < 4:
            flash('Family Name must be greater than 3 characters', category='error')
        elif password != password_confirm:
            flash('Passwords do not match', category='error')
        elif len(password) < 8:
            flash('Password must be greater than 7 characters', category='error')
        elif full_address_complete is False:
            flash('Address must not have empty fields', category='error')
        else:
            password_hash = generate_password_hash(password, method='sha256')
            cursor = connect.cursor()
            cursor.execute(
                '''INSERT INTO users (first_name, family_name, email, password, address)
                VALUES ('%s', '%s', '%s', '%s', '%s')'''
                % (first_name, family_name, email, password_hash, full_address))
            connect.commit()
            cursor.close()
            connect.close()
            flash('Account successfully created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("register.html",  datetime=str(datetime.now().year))
