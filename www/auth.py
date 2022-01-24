from flask import Blueprint, render_template, request, flash
from datetime import datetime

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html",  datetime=str(datetime.now().year))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        fullName = request.form.get('fullName')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')

        if len(email) < 4:
            flash('Email must be greater 3 characters', category='error')
        elif len(fullName) < 4:
            flash('Full Name must be greater than 3 characters', category='error')
        elif password != passwordConfirm:
            flash('Passwords do not match', category='error')
        elif len(password) < 8:
            flash('Password must be greater than 7 characters', category='error')
        else:
            flash('Account successfully created!', category='success')

    return render_template("register.html",  datetime=str(datetime.now().year))
