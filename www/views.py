from flask import Blueprint, render_template
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/')
def root():
    return render_template("home.html", datetime=str(datetime.now().year))


# @views.route('/home')
# def home():
#     return render_template("home.html", datetime=str(datetime.now().year))
#
#
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
