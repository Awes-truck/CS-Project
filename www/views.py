from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from datetime import datetime
from urllib.parse import urlparse
from .__init__ import sql_connect
import stripe
from textmagic.rest import TextmagicRestClient
import os

views = Blueprint('views', __name__)

# Assign constant variables
SQL_HOST = os.getenv("SQL_HOST")
SQL_PORT = int(os.getenv("SQL_PORT"))
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
SQL_DATABASE = os.getenv("SQL_DATABASE")
stripe.api_key = os.getenv('STRIPE_API_TEST_SK')
TEXTMAGIC_USERNAME = os.getenv('TEXTMAGIC_USERNAME')
TEXTMAGIC_API_KEY = os.getenv('TEXTMAGIC_API_KEY')

# Create a database conenction
CONNECT = sql_connect(
    SQL_HOST,
    SQL_PORT,
    SQL_USER,
    SQL_PASSWORD,
    SQL_DATABASE
)

# Create a dictionary with subscription information and flags
# Key: name value: [group id, price id, flag type]
price_dict = {
    'social': ['3', 'price_1KTT07HuaTKPzffSkYKw4EPw', 'senior_flag'],
    'senior': ['4', 'price_1KTNDVHuaTKPzffS1ubgGAr7', 'senior_flag'],
    'senior_edu': ['5', 'price_1KTS4HHuaTKPzffSsYTpJcNQ', 'senior_flag'],
    'junior': [None, 'price_1KTOPyHuaTKPzffS5yvO1LSb', 'junior_flag'],
    'junior_dev': [None, 'price_1KTnk8HuaTKPzffSo8JBgFX2', 'junior_flag']
}


@views.route('/')
def home():
    return render_template("home.html", DATETIME=str(datetime.now().year))


@views.route('/subscriptions', methods=['GET', 'POST'])
def subscriptions():
    # DEVELOPMENT PURPOSES
    url = urlparse(request.base_url)
    hostname = url.hostname
    port = ''
    if hostname == 'localhost':
        port = ':5000'
    else:
        port = ':80'

    # Retrieve POST request content
    if request.method == "POST":
        # Check if user is logged in
        if 'loggedin' not in session:
            flash('You must be logged in to make purchases', category='error')
            return redirect(url_for('auth.login'))
        '''
        Initialise a variable and loop through our dictionary to verify if the
        price_ids for the products on the page match and then assign it to our
        variable
        '''
        price_id = None
        for k, v in price_dict.items():
            if request.form.get(k):
                price_id = v[1]
        if price_id is None:
            flash(
                # Products are misconfigured and need manual changes
                "There was an error - please contact the system administrator",
                category='error')
            return redirect(url_for('views.home'))

        # Create a new stripe session to proceed with payment
        stripe_session = stripe.checkout.Session.create(
            # Assign the payment to the users email
            customer_email=session['email'],
            # Subscription that intends to be bought using the price_id...
            # ...retrieved from the loop
            line_items=[{
                'price': price_id,
                'quantity': 1
            }],
            # Save the user id for future record
            metadata={'user_id': session['id']},
            # Specify that the session is for a subscription to...
            # ...setup auto-payments
            mode='subscription',
            # On success, redirect to our success page
            # We also want to put our price id in the url as an argument for...
            # ...later use on the success page
            success_url='http://%s%s/success?session_id={CHECKOUT_SESSION_ID}&price_id=%s'
            % (hostname, port, price_id),
            # If the user cancels the payment, redirect back to original page
            cancel_url='http://%s%s/subscriptions'
            % (hostname, port)
        )
        # Create a new session variable with the id of the Stripe Sesssion
        session['stripe_session'] = stripe_session.id

        # Loop through our dictionary and do some conditions and checks
        for k, v in price_dict.items():
            # If a key has a Junior Flag and the price_id matches our...
            # ...session, get POST content and assign them to some variables
            if v[2] == 'junior_flag' and v[1] == price_id:
                first_name = request.form.get('junior_first_name')
                family_name = request.form.get('junior_family_name')
                birthdate = request.form.get('junior_dob')
                if len(first_name) < 4:
                    flash('First Name must be greater than 3 characters',
                          category='error')
                    break
                elif len(family_name) < 4:
                    flash('Family Name must be greater than 3 characters',
                          category='error')
                    break
                elif birthdate == '':
                    flash('Please insert a Date of Birth', category='error')
                    break
                elif birthdate > str(datetime.now()):
                    flash('Date cannot be in the future', category='error')
                    break
                else:
                    # All conditions have passed, create new session...
                    # .. variables to be used on the Success page
                    session['junior_first_name'] = request.form.get(
                        'junior_first_name')
                    session['junior_family_name'] = request.form.get(
                        'junior_family_name')
                    session['junior_dob'] = request.form.get('junior_dob')
        # Redirect to the third-party Stripe Session page
        return redirect(stripe_session.url, code=303)
    return render_template("subscriptions.html", DATETIME=str(datetime.now().year))


@views.route('/success')
def success():
    if 'loggedin' not in session:
        flash("You are not logged in!", category='error')
        return redirect(url_for('auth.login'))
    # Conditions too long for one line, split them up a bit for readability
    check_session_exists = 'stripe_session' not in session
    check_id_in_args = 'session_id' not in request.args
    check_session_query = session['stripe_session'] != request.args.get(
        'session_id')
    # We don't want users to access the success page without actually buying...
    # ...anything
    if check_session_exists or check_id_in_args or check_session_query:
        flash("You cannot access this page from here", category='error')
        return redirect(url_for('views.home'))

    # Retrieve both the product, and its price from the Stripe Session
    item = stripe.checkout.Session.list_line_items(session['stripe_session'])
    product = item.data[0].price.product
    product = stripe.Product.retrieve(product).name
    price = item.data[0].price.id
    price = stripe.Price.retrieve(price).unit_amount
    # Price comes unformatted, let's fix that
    price = format(price / 100, '.02f')

    # We no longer need the Stripe Session, garbage collect
    session.pop('stripe_session', None)

    # Assign some variables from our session that we plan to use
    id = session['id']
    name = session['name']

    # SMS Notification of successful payment
    # Check if the user even has a phone number connected to the account
    if 'phone' in session:
        # Try to send a message (it ignores the condition for some reason)
        try:
            phone = session['phone'].replace('+', '')
            print(phone)
            client = TextmagicRestClient(TEXTMAGIC_USERNAME, TEXTMAGIC_API_KEY)
            client.messages.create(
                phones=phone,
                text=f"Hi, {name}. Your purchase of '{product}' for £{price} was successful!"
            )
        except:
            # Send was unsuccessful, just carry on
            pass

    # Create a database instance
    cursor = CONNECT.cursor()
    # Loop through our dictionary again
    for k, v in price_dict.items():
        # Check if the subscription is a senior one and grab the arg from...
        # ..the success url
        if v[2] == 'senior_flag' and v[1] == request.args.get('price_id'):
            # Update the user's group with the corresponding ID from the dict
            cursor.execute('''
                UPDATE seniors
                SET group_id = '%s'
                WHERE senior_id = '%s'
            ''' % (v[0], id))
            # Commit the change
            CONNECT.commit()
            cursor.close()
        # If the subscription is a junior one and the price id matches...
        elif v[2] == 'junior_flag' and v[1] == request.args.get('price_id'):
            # ...set some variables from our session variables
            junior_first_name = session['junior_first_name']
            junior_family_name = session['junior_family_name']
            junior_dob = session['junior_dob']

            # If the key is the junior subscription...
            if k == 'junior':
                # ...Insert our session data into the database
                cursor.execute('''
                    INSERT INTO juniors
                        (first_name, family_name, dob, senior_id)
                    VALUES
                        ('%s', '%s', '%s', '%s')
                ''' % (junior_first_name, junior_family_name, junior_dob, id))
                # Commit changes
                CONNECT.commit()
                cursor.close()
            # If the key is the developmental junior subscription...
            elif k == 'junior_dev':
                # Insert data into the datbase and set 'is_developmental' to 1
                cursor.execute('''
                    INSERT INTO juniors
                        (first_name, family_name, dob, senior_id, is_developmental)
                    VALUES
                        ('%s', '%s', '%s', '%s', 1)
                ''' % (junior_first_name, junior_family_name, junior_dob, id))
                # Save changes
                CONNECT.commit()
                cursor.close()
            # Garbage collection
            session.pop('junior_first_name', None)
            session.pop('junior_family_name', None)
            session.pop('junior_dob', None)

    return render_template("success.html", DATETIME=str(datetime.now().year))
