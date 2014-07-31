from flask import render_template, redirect, g, request, url_for
from flask_login import current_user, login_user

from app import app, db, login_manager
from app.models import User
from app.forms import LoginForm


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def home():
    return "Hello world!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home'))
    form = LoginForm()
    errors = []
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.verify_password(form.password.data):
                login_user(user)
            else:
                errors.append('Invalid password!')
        else:
            errors.append('Invalid username!')
    else:
        errors.append('Please complete the form!')
    return render_template('login.html', form=form, errors=errors)