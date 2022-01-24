from flask import Blueprint, render_template, request
from datetime import datetime

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html",  datetime=str(datetime.now().year))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # if request.method == 'POST':
    #     email = request.form.get('email')
    #     fullName = request.form.get('fullName')
    #     password = request.form.get('password')
    #     passwordConfirm = request.form.get('passwordConfirm')

        return render_template("register.html",  datetime=str(datetime.now().year))
