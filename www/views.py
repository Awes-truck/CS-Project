from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from datetime import datetime
from urllib.parse import urlparse
from .__init__ import sql_connect, login_required
import stripe
from textmagic.rest import TextmagicRestClient
import os

views = Blueprint('views', __name__)

SQL_HOST = os.getenv("SQL_HOST")
SQL_PORT = int(os.getenv("SQL_PORT"))
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
SQL_DATABASE = os.getenv("SQL_DATABASE")
stripe.api_key = os.getenv('STRIPE_API_TEST_SK')
TEXTMAGIC_USERNAME = os.getenv('TEXTMAGIC_USERNAME')
TEXTMAGIC_API_KEY = os.getenv('TEXTMAGIC_API_KEY')

CONNECT = sql_connect(
    SQL_HOST,
    SQL_PORT,
    SQL_USER,
    SQL_PASSWORD,
    SQL_DATABASE
)

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
    url = urlparse(request.base_url)
    hostname = url.hostname
    port = ''
    if hostname == 'localhost':
        port = ':5000'
    else:
        port = ':80'

    if request.method == "POST":
        if 'loggedin' not in session:
            flash('You must be logged in to make purchases', category='error')
            return redirect(url_for('auth.login'))

        price_id = None
        for k, v in price_dict.items():
            if request.form.get(k):
                price_id = v[1]
        if price_id is None:
            flash(
                "There was an error - please contact the system administrator",
                category='error')
            return redirect(url_for('views.home'))

        stripe_session = stripe.checkout.Session.create(
            customer_email=session['email'],
            line_items=[{
                'price': price_id,
                'quantity': 1
            }],
            metadata={'user_id': session['id']},
            mode='subscription',
            success_url='http://%s%s/success?session_id={CHECKOUT_SESSION_ID}&price_id=%s'
            % (hostname, port, price_id),
            cancel_url='http://%s%s/subscriptions'
            % (hostname, port)
        )
        session['stripe_session'] = stripe_session.id

        for k, v in price_dict.items():
            if v[2] == 'j' and v[1] == price_id:
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
                    session['junior_first_name'] = request.form.get(
                        'junior_first_name')
                    session['junior_family_name'] = request.form.get(
                        'junior_family_name')
                    session['junior_dob'] = request.form.get('junior_dob')

        return redirect(stripe_session.url, code=303)
    return render_template("subscriptions.html", DATETIME=str(datetime.now().year))


@views.route('/success')
@login_required
def success():
    check_session_exists = 'stripe_session' not in session
    check_id_in_args = 'session_id' not in request.args
    check_session_query = session['stripe_session'] != request.args.get(
        'session_id')

    if check_session_exists or check_id_in_args or check_session_query:
        flash("You cannot access this page from here", category='error')
        return redirect(url_for('views.home'))

    item = stripe.checkout.Session.list_line_items(session['stripe_session'])
    product = item.data[0].price.product
    product = stripe.Product.retrieve(product).name
    price = item.data[0].price.id
    price = stripe.Price.retrieve(price).unit_amount
    format(price / 100, '.02f')

    session.pop('stripe_session', None)
    id = session['id']
    name = session['name']

    if 'phone' in session:
        try:
            phone = session['phone'].replace('+', '')
            print(phone)
            client = TextmagicRestClient(TEXTMAGIC_USERNAME, TEXTMAGIC_API_KEY)
            client.messages.create(
                phones=phone,
                text=f"Hi, {name}. Your purchase of '{product}' for £{price} was successful!"
            )
        except:
            pass

    cursor = CONNECT.cursor()
    for k, v in price_dict.items():
        if v[2] == 'senior_flag' and v[1] == request.args.get('price_id'):
            cursor.execute('''
                UPDATE seniors
                SET group_id = '%s'
                WHERE senior_id = '%s'
            ''' % (v[0], session['id']))
            CONNECT.commit()
            cursor.close()
        elif v[2] == 'junior_flag' and v[1] == request.args.get('price_id'):
            junior_first_name = session['junior_first_name']
            junior_family_name = session['junior_family_name']
            junior_dob = session['junior_dob']

            if k == 'junior':
                cursor.execute('''
                    INSERT INTO juniors
                        (first_name, family_name, dob, senior_id)
                    VALUES
                        ('%s', '%s', '%s', '%s')
                ''' % (junior_first_name, junior_family_name, junior_dob, id))
                CONNECT.commit()
                cursor.close()
            elif k == 'junior_dev':
                cursor.execute('''
                    INSERT INTO juniors
                        (first_name, family_name, dob, senior_id, is_developmental)
                    VALUES
                        ('%s', '%s', '%s', '%s', 1)
                ''' % (junior_first_name, junior_family_name, junior_dob, id))
                CONNECT.commit()
                cursor.close()
            session.pop('junior_first_name', None)
            session.pop('junior_family_name', None)
            session.pop('junior_dob', None)

    return render_template("success.html", DATETIME=str(datetime.now().year))
