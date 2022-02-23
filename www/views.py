from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from datetime import datetime
from urllib.parse import urlparse
from .__init__ import sql_connect, login_required
import stripe
import os

views = Blueprint('views', __name__)

SQL_HOST = os.getenv("SQL_HOST")
SQL_PORT = int(os.getenv("SQL_PORT"))
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
SQL_DATABASE = os.getenv("SQL_DATABASE")
stripe.api_key = os.getenv('STRIPE_API_TEST_SK')

connect = sql_connect(
    SQL_HOST,
    SQL_PORT,
    SQL_USER,
    SQL_PASSWORD,
    SQL_DATABASE
)


@views.route('/')
def home():
    return render_template("home.html", datetime=str(datetime.now().year))


@views.route('/subscriptions', methods=['GET', 'POST'])
def subscriptions():
    url = urlparse(request.base_url)
    hostname = url.hostname
    port = ''
    if hostname == 'localhost':
        port = ':5000'
    else:
        port = ':80'

    price_dict = {
        'senior': 'price_1KTNDVHuaTKPzffS1ubgGAr7',
        'senior_edu': 'price_1KTS4HHuaTKPzffSsYTpJcNQ',
        'social': 'price_1KTT07HuaTKPzffSkYKw4EPw',
        'junior': 'price_1KTOPyHuaTKPzffS5yvO1LSb',
        'junior_dev': 'price_1KTnk8HuaTKPzffSo8JBgFX2'
    }

    if request.method == "POST":
        if 'loggedin' not in session:
            flash('You must be logged in to make purchases', category='error')
            return redirect(url_for('auth.login'))

        price_id = None
        for k, v in price_dict.items():
            if request.form.get(k):
                price_id = v
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
            success_url='http://%s%s/success?session_id={CHECKOUT_SESSION_ID}&price_id=%s' %
            (hostname, port, price_id),
            cancel_url='http://%s%s/subscriptions' % (hostname, port)
        )
        session['stripe_session'] = stripe_session.id
        return redirect(stripe_session.url, code=303)
    return render_template("subscriptions.html", datetime=str(datetime.now().year))


@views.route('/success')
@login_required
def success():
    if 'stripe_session' not in session or 'session_id' not in request.args or session['stripe_session'] != request.args.get('session_id'):
        flash("You cannot access this page from here", category='error')
        return redirect(url_for('views.home'))
    session.pop('stripe_session', None)

    # check if product is junior or senior
    product = request.args.get('price_id')
    # if product ==
    # if senior, update via session['email'] (user) with new usergroup
    return render_template("success.html", datetime=str(datetime.now().year))
# @views.route('/index')
# def index():
#     return render_template("home.html", datetime=str(datetime.now().year))
#
#
# @views.route('/projects')
# def projects():
#   return render_template("projects.html", datetime=str(datetime.now().year))
#
#
# @views.route('/about')
# def about():
#     return render_template("about.html", datetime=str(datetime.now().year))
#
#
# @views.route('/contact')
# def contact():
#     return render_template("contact.html", datetime=str(datetime.now().year))
