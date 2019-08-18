from flask import render_template, Blueprint, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return redirect(url_for('users.register'))