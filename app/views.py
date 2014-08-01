from flask import render_template, redirect, g, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from config import BEANS_PER_PAGE, BREWS_PER_PAGE, ROASTS_PER_PAGE
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
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.verify_password(form.password.data):
                login_user(user)
                return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(username=form.username.data, password=User.hash_password(form.password.data))
            User.add_user(user)
            login_user(user)
            return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/bean/add', methods=['GET', 'POST'])
@login_required
def bean_add():
    form = BeanPurchaseForm()
    user = g.user
    if form.validate_on_submit():
        bean = Bean(
            name=form.name.data, bean_type=form.type.data,
            weight=form.weight.data, purchase_date=form.purchase_date.data,
            notes=form.notes.data, user_id=user.id)
        Bean.add_bean(bean)
        return redirect(url_for('bean_list'))
    return render_template('bean_add.html', form=form)


@app.route('/bean/list')
@app.route('/bean/list/<int:page>')
@login_required
def bean_list(page=1):
    user = g.user
    beans = Bean.query.filter_by(user_id=user.id).order_by(Bean.purchase_date.desc()).paginate(
        page, BEANS_PER_PAGE, False)
    return render_template('bean_list.html', beans=beans)


@app.route('/brew/add', methods=['GET', 'POST'])
@login_required
def brew_add():
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
        return redirect(url_for('brew_list'))
    return render_template('brew_add.html', form=form)


@app.route('/brew/list')
@app.route('/brew/list/<int:page>')
@login_required
def brew_list(page=1):
    user = g.user
    brews = Brew.query.filter_by(user_id=user.id).order_by(Brew.brew_date.desc()).paginate(page, BREWS_PER_PAGE, False)
    return render_template('brew_list.html', brews=brews)


@app.route('/roast/add', methods=['GET', 'POST'])
@login_required
def roast_add():
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
        return redirect(url_for('roast_list'))
    return render_template('roast_add.html', form=form)


@app.route('/roast/list')
@app.route('/roast/list/<int:page>')
@login_required
def roast_list(page=1):
    user = g.user
    roasts = Roast.query.filter_by(user_id=user.id).order_by(Roast.roast_date.desc()).paginate(
        page, ROASTS_PER_PAGE, False)
    return render_template('roast_list.html', roasts=roasts)