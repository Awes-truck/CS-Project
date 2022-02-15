from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from datetime import datetime
from urllib.parse import urlparse
import stripe
import os
stripe.api_key = os.getenv('STRIPE_API_TEST_SK')
views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", datetime=str(datetime.now().year))


@views.route('/news')
def news():
    return render_template("news.html", datetime=str(datetime.now().year))


@views.route('/subscriptions', methods=['GET', 'POST'])
def subscriptions():
    url = urlparse(request.base_url)
    hostname = url.hostname
    port = ''
    price_id = ''
    if hostname == 'localhost':
        port = ':5000'
    else:
        port = ':80'
    if request.method == "POST":
        if 'loggedin' not in session:
            flash('You must be logged in to make purchases', category='error')
            return redirect(url_for('auth.login'))
        if request.form.get('senior'):
            price_id = 'price_1KTNDVHuaTKPzffS1ubgGAr7'
        elif request.form.get('senior_edu'):
            price_id = 'price_1KTS4HHuaTKPzffSsYTpJcNQ'
        elif request.form.get('junior'):
            price_id = 'price_1KTOPyHuaTKPzffS5yvO1LSb'
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
            success_url='http://' + hostname + port + '/subscriptions',
            cancel_url='http://' + hostname + port + '/subscriptions'
        )
        return redirect(stripe_session.url, code=303)
    return render_template("subscriptions.html", datetime=str(datetime.now().year))


# @views.route('/payment', methods=['GET', 'POST'])
# def payment():
#     if request.method == "POST":
#         if request.form.get('senior'):
#             print("Senior test")
#             stripe_session = stripe.checkout.Session.create(
#                 line_items=[{
#                     'price': 'price_1KTNDVHuaTKPzffS1ubgGAr7',
#                     'quantity': 1
#                 }],
#                 mode='payment',
#                 success_url=url_for('views.home'),
#                 cancel_url=url_for('views.home')
#             )
#             return redirect(stripe_session.url, code=303)
#         if request.form.get('junior'):
#             print("Junior test")
#             stripe_session = stripe.checkout.Session.create(
#                 line_items=[{
#                     'price': 'price_1KTOPyHuaTKPzffS5yvO1LSb',
#                     'quantity': 1
#                 }],
#                 mode='payment',
#                 success_url=url_for('views.home'),
#                 cancel_url=url_for('views.home')
#             )
#             return redirect(stripe_session.url, code=303)
#         print("Test3")
#     return render_template("subscriptions.html", datetime=str(datetime.now().year))


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
