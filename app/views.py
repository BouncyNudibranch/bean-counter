from flask import render_template, redirect, g, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db, login_manager
from app.models import User, Bean
from app.forms import LoginForm, RegisterForm, BeanPurchaseForm


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
                return redirect(url_for('home'))
            else:
                errors.append('Invalid password!')
        else:
            errors.append('Invalid username!')
    else:
        errors.append('Please complete the form!')
    return render_template('login.html', form=form, errors=errors)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home'))
    form = RegisterForm()
    errors = []
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(username=form.username.data, password=User.hash_password(form.password.data))
            User.add_user(user)
            login_user(user)
            return redirect(url_for('home'))
        else:
            errors.append('Username already exists!')
    else:
        errors.append('Please complete the form!')
    return render_template('register.html', form=form, errors=errors)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/bean_purchase', methods=['GET', 'POST'])
@login_required
def bean_purchase():
    form = BeanPurchaseForm()
    user = g.user
    if form.validate_on_submit():
        bean = Bean(
            name=form.name.data, bean_type=form.type.data,
            weight=form.weight.data, purchase_date=form.purchase_date.data,
            notes=form.notes.data, user_id=user.id)
        Bean.add_bean(bean)
        # return redirect(url_for('home'))
    bean_purchases = Bean.query.filter_by(user_id=user.id).order_by(Bean.purchase_date.desc()).limit(10).all()
    return render_template('bean_purchase.html', form=form, bean_purchases=bean_purchases)