from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from datetime import datetime
from urllib.parse import urlparse
from .__init__ import sql_connect, login_required
import stripe
import os
stripe.api_key = os.getenv('STRIPE_API_TEST_SK')
views = Blueprint('views', __name__)


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
    if request.method == "POST":
        if 'loggedin' not in session:
            flash('You must be logged in to make purchases', category='error')
            return redirect(url_for('auth.login'))

        price_id = ''
        if request.form.get('senior'):
            price_id = 'price_1KTNDVHuaTKPzffS1ubgGAr7'
        elif request.form.get('senior_edu'):
            price_id = 'price_1KTS4HHuaTKPzffSsYTpJcNQ'
        elif request.form.get('social'):
            price_id = 'price_1KTT07HuaTKPzffSkYKw4EPw'
        elif request.form.get('junior'):
            price_id = 'price_1KTOPyHuaTKPzffS5yvO1LSb'
        elif request.form.get('junior_dev'):
            price_id = 'price_1KTnk8HuaTKPzffSo8JBgFX2'
        else:
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
            mode='subscription',
            success_url='http://' + hostname + port
            + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://' + hostname + port + '/subscriptions'
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
    stripe_session = stripe.checkout.Session.retrieve(
        request.args.get('session_id')
    )
    session.pop('stripe_session', None)

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
