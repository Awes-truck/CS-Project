from flask import Blueprint, render_template, redirect, session, url_for, request, flash, current_app as app
from datetime import datetime
from .__init__ import sql_connect
import os
import stripe
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

SQL_HOST = os.getenv("SQL_HOST")
SQL_PORT = int(os.getenv("SQL_PORT"))
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
SQL_DATABASE = os.getenv("SQL_DATABASE")
stripe.api_key = os.getenv("STRIPE_API_TEST_SK")

connect = sql_connect(
    SQL_HOST,
    SQL_PORT,
    SQL_USER,
    SQL_PASSWORD,
    SQL_DATABASE
)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        flash('You\'re already logged in!', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = connect.cursor()
        user = cursor.execute(
            '''SELECT senior_id, password, first_name FROM seniors WHERE email='%s' '''
            % email
        )
        user = cursor.fetchone()
        cursor.close()
        if user:
            # Not used, but still needs to be declared to work for some reason
            user_id = user[0]
            user_password_hash = user[1]
            user_name = user[2]
            if check_password_hash(user_password_hash, password):
                session.permanent = True
                session['loggedin'] = True
                session['email'] = email
                session['name'] = user_name
                session['id'] = user_id
                flash('Logged in Successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Please try again!', category='error')
        else:
            flash('Incorrect email. Please try again!', category='error')
    return render_template("login.html",  datetime=str(datetime.now().year))


@auth.route('/logout')
def logout():
    session_vars = [
        'email',
        'name',
        'loggedin',
        'id'
    ]
    if session['loggedin']:
        for i in session_vars:
            session.pop(i, None)
    return redirect(url_for('views.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if 'loggedin' in session:
        flash('Logout to access this page!', category='error')
        return redirect(url_for('views.home'))

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
        phone_number = request.form.get('phone')

        cursor = connect.cursor()
        query = cursor.execute(
            '''SELECT email FROM seniors WHERE email = '%s' ''' % email)
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
                '''INSERT INTO seniors (first_name, family_name, email, password, address, phone_number)
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s')'''
                % (first_name, family_name, email, password_hash, full_address, phone_number))
            connect.commit()
            cursor.close()
            flash('Account successfully created!', category='success')
            stripe.Customer.create(
                description=" ",
                address={
                    'line1': request.form.get(postal_keys[0]),
                    'line2': request.form.get(postal_keys[1]),
                    'city': request.form.get(postal_keys[2]),
                    'state': request.form.get(postal_keys[3]),
                    'postal_code': request.form.get(postal_keys[4])
                },
                name=" ".join([first_name, family_name]),
                email=email,
                phone=phone_number
            )

            return redirect(url_for('views.home'))

    return render_template("register.html",  datetime=str(datetime.now().year))
