from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html')

# Na razie tak a, jak któreś będzie potrzebowało rozbudowy to się doda osoby package
@main.route('/lights')
@login_required
def lights():
    return render_template('lights.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# @main.route('/settings')
# @login_required
# def settings():
#     return render_template('settings.html')