from flask import render_template, redirect, g, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db, login_manager
from app.models import User, Bean, Brew, Roast
from app.forms import LoginForm, RegisterForm, BeanPurchaseForm, BrewForm, RoastForm


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def home():
    return render_template('home.html')


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
    bean_purchases = Bean.query.filter_by(user_id=user.id).order_by(Bean.purchase_date.desc()).limit(10).all()
    return render_template('bean_purchase.html', form=form, bean_purchases=bean_purchases)


@app.route('/brew', methods=['GET', 'POST'])
@login_required
def brew():
    user = g.user
    form = BrewForm()
    form.roast_batch.choices = [(r.id, '%s - %s' % (r.roast_date, r.bean.name)) for r in Roast.query.filter_by(
        user_id=user.id).order_by(Roast.roast_date.desc()).limit(10).all()]
    form.roast_batch.choices.append((0, 'N/A'))
    form.bean_id.choices = [(b.id, '%s - %s (%dg)' % (b.purchase_date, b.name, b.weight)) for b in Bean.query.filter_by(
        user_id=user.id).order_by(Bean.purchase_date.desc()).limit(10).all()]
    if form.validate_on_submit():
        _brew = Brew(
            grind_size=form.grind_size.data, bean_dose=form.bean_dose.data, water_dose=form.water_dose.data,
            extraction_time=form.extraction_time.data, brew_method=form.brew_method.data,
            filter_type=form.filter_type.data, brew_date=form.brew_date.data, notes=form.notes.data,
            user_id=user.id, bean_id=form.bean_id.data
        )
        if form.roast_batch.data != 0:
            _brew.roast_id = form.roast_batch.data
        Brew.add_brew(_brew)
    past_brews = Brew.query.filter_by(user_id=user.id).order_by(Brew.brew_date.desc()).limit(10).all()
    return render_template('brew.html', form=form, past_brews=past_brews)


@app.route('/roast', methods=['GET', 'POST'])
@login_required
def roast():
    user = g.user
    form = RoastForm()
    form.bean_id.choices = [(b.id, '%s - %s (%dg)' % (b.purchase_date, b.name, b.weight)) for b in Bean.query.filter_by(
        user_id=user.id).order_by(Bean.purchase_date.desc()).limit(10).all()]
    if form.validate_on_submit():
        _roast = Roast(
            bean_dose=form.bean_dose.data, drop_temp=form.drop_temp.data, dry_end_time=form.dry_end_time.data,
            dry_end_temp=form.dry_end_temp.data, fc_begin_time=form.fc_begin_time.data,
            fc_begin_temp=form.fc_begin_temp.data, fc_end_time=form.fc_end_time.data, fc_end_temp=form.fc_end_temp.data,
            sc_begin_time=form.sc_begin_time.data, sc_begin_temp=form.sc_begin_temp.data,
            sc_end_time=form.sc_end_time.data, sc_end_temp=form.sc_end_temp.data, end_time=form.end_time.data,
            end_temp=form.end_temp.data, end_weight=form.end_weight.data, roaster_machine=form.roaster_machine.data,
            roast_date=form.roast_date.data, notes=form.notes.data, bean_id=form.bean_id.data, user_id=user.id
        )
        Roast.add_roast(_roast)
    past_roasts = Roast.query.filter_by(user_id=user.id).order_by(Roast.roast_date.desc()).limit(10).all()
    return render_template('roast.html', form=form, past_roasts=past_roasts)