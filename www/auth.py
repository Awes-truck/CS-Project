from flask import Blueprint, render_template, request, flash
from datetime import datetime

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
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
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        family_name = request.form.get('family_name')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        for i in postal_keys:
            full_address_list.append(request.form.get(i))

        full_address = separator.join(full_address_list)

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
            flash('Account successfully created!', category='success')

    return render_template("register.html",  datetime=str(datetime.now().year))
