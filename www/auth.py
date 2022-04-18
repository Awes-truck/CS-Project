from flask import Blueprint, render_template, redirect, session, url_for, request, flash, current_app as app
from datetime import datetime
from .__init__ import sql_connect
import os
import stripe
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# Assign constant variables
SQL_HOST = os.getenv("SQL_HOST")
SQL_PORT = int(os.getenv("SQL_PORT"))
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
SQL_DATABASE = os.getenv("SQL_DATABASE")
stripe.api_key = os.getenv("STRIPE_API_TEST_SK")

# Create a database conenction
CONNECT = sql_connect(
    SQL_HOST,
    SQL_PORT,
    SQL_USER,
    SQL_PASSWORD,
    SQL_DATABASE
)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Check if the user is logged in and redirect home if is the case
    if 'loggedin' in session:
        flash('You\'re already logged in!', category='error')
        return redirect(url_for('views.home'))
    # Get the POST request content
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Connect to a database instance
        cursor = CONNECT.cursor()

        # Retreive the user if the email exists in the database
        cursor.execute(
            '''SELECT senior_id, password, first_name, phone_number FROM seniors WHERE email='%s' '''
            % email
        )
        user = cursor.fetchone()
        cursor.close()

        # We have a valid user
        if user:
            # Store their relevant information in variables from the db query
            user_id = user[0]
            user_password_hash = user[1]
            user_name = user[2]
            phone_number = user[3]

            # Check the password hash input matches the password hash stored
            if check_password_hash(user_password_hash, password):
                # Store the session variables and keep persistence
                session.permanent = True
                session['loggedin'] = True
                session['email'] = email
                session['name'] = user_name
                session['id'] = user_id
                if phone_number is not None:
                    session['phone'] = phone_number
                # User has successfully logged in
                flash('Logged in Successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                # User entered an incorrect password and forced to try again
                flash('Incorrect password. Please try again!', category='error')

        # User doesn't exist in the database
        else:
            flash('Incorrect email. Please try again!', category='error')
    return render_template("login.html", DATETIME=str(datetime.now().year))


@auth.route('/logout')
def logout():
    # Clear all session variables and redirect home if user is logged in
    if 'loggedin' not in session:
        flash("You are not logged in!", category='error')
        return redirect(url_for('auth.login'))

    session.clear()

    return redirect(url_for('views.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Check if the user is already logged into an account
    if 'loggedin' in session:
        flash('Logout to access this page!', category='error')
        return redirect(url_for('views.home'))

    '''
    A list of address values found in register.html. We'll loop through this to
    to fetch values in our POST request.This will be used to create a complete
    address when adding to the database.
    '''
    postal_keys = [
        'address1',
        'postal_town',
        'administrative_area_level_2',
        'postal_code'
    ]
    # Initialise an empty list that will populated with our address values
    full_address_list = []
    # Separator for the join function that will format the address properly
    separator = ', '
    # Assign a vriable with a True value that will be used as a condition...
    # ...for checking whether the address is complete and the user can proceed
    full_address_complete = True
    # Assign a variable assuming the email the user input doesn't exist already
    email_exists = False

    # Retreive POST request content
    if request.method == 'POST':
        email = str(request.form.get('email'))
        first_name = request.form.get('first_name')
        family_name = request.form.get('family_name')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        # Check if user input a phone number as it's not required
        if request.form.get('phone') is not None:
            phone_number = request.form.get('phone')
        else:
            phone_number = "NULL"

        '''
        Loop through our list and check all address fields have been
        filled out. If so, create our full address using .join(). If not, set
        full_address_complete to False and break out of the loop and force the
        user to try again
        '''
        for i in postal_keys:
            if request.form.get(i) is None:
                full_address_complete = False
                break
            else:
                full_address_list.append(str(request.form.get(i)))

        if full_address_complete:
            full_address = separator.join(full_address_list)

        # Create a database instance
        cursor = CONNECT.cursor()
        # Check if the email already exists in our database
        query = cursor.execute(
            '''SELECT email FROM seniors WHERE email = '%s' ''' % email)
        # If a result returns, set our pre-existing variable to True
        if query != 0:
            email_exists = True
        cursor.close()

        # Create some conditions and checks
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
            # Encrypt the user password
            password_hash = generate_password_hash(password, method='sha256')
            # Create a database instance
            cursor = CONNECT.cursor()
            # Insert all our user data into the database
            cursor.execute(
                '''INSERT INTO seniors (first_name, family_name, email, password, address, phone_number, group_id)
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 2)'''
                % (first_name, family_name, email, password_hash, full_address, phone_number))
            # Commit our new change
            CONNECT.commit()
            cursor.close()
            flash('Account successfully created!', category='success')

            return redirect(url_for('views.home'))

    return render_template("register.html", DATETIME=str(datetime.now().year))
