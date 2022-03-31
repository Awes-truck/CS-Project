from flask import Blueprint, render_template, redirect, session, url_for, request, flash, current_app as app
from datetime import datetime
from .__init__ import sql_connect, login_required
import os
import stripe
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

DATETIME = str(datetime.now().year)
SQL_HOST = os.getenv("SQL_HOST")
SQL_PORT = int(os.getenv("SQL_PORT"))
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
SQL_DATABASE = os.getenv("SQL_DATABASE")
stripe.api_key = os.getenv("STRIPE_API_TEST_SK")

CONNECT = sql_connect(
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

        cursor = CONNECT.cursor()
        cursor.execute(
            '''SELECT senior_id, password, first_name, phone_number FROM seniors WHERE email='%s' '''
            % email
        )
        user = cursor.fetchone()
        cursor.close()
        if user:
            user_id = user[0]
            user_password_hash = user[1]
            user_name = user[2]
            phone_number = user[3]

            if check_password_hash(user_password_hash, password):
                session.permanent = True
                session['loggedin'] = True
                session['email'] = email
                session['name'] = user_name
                session['id'] = user_id
                if not phone_number == '':
                    session['phone'] = phone_number
                print(type(session['phone']))
                flash('Logged in Successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Please try again!', category='error')
        else:
            flash('Incorrect email. Please try again!', category='error')
    return render_template("login.html", DATETIME)


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('views.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if 'loggedin' in session:
        flash('Logout to access this page!', category='error')
        return redirect(url_for('views.home'))

    postal_keys = [
        'address1',
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
        if request.form.get('phone') == '':
            phone_number = None
        else:
            phone_number = request.form.get('phone')
        cursor = CONNECT.cursor()
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
            cursor = CONNECT.cursor()
            cursor.execute(
                '''INSERT INTO seniors (first_name, family_name, email, password, address, phone_number, group_id)
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 2)'''
                % (first_name, family_name, email, password_hash, full_address, phone_number))

            user_id = str(cursor.lastrowid)
            CONNECT.commit()
            cursor.close()
            flash('Account successfully created!', category='success')
            stripe.Customer.create(
                description="User ID: " + user_id,
                address={
                    'line1': request.form.get(postal_keys[0]),
                    'city': request.form.get(postal_keys[1]),
                    'state': request.form.get(postal_keys[2]),
                    'postal_code': request.form.get(postal_keys[3])
                },
                name=" ".join([first_name, family_name]),
                email=email,
                phone=phone_number
            )

            email_exists = False
            return redirect(url_for('views.home'))

    return render_template("register.html", DATETIME)
