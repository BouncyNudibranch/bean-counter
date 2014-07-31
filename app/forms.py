from datetime import date, datetime
from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, SelectField, DateField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, EqualTo, Optional
from app.models import BEAN_TYPES, GRIND_SIZES, BREW_METHODS, FILTER_TYPES


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Password Confirmation', validators=[
        DataRequired(), EqualTo('password', message='Passwords do not match!')])


class BeanPurchaseForm(Form):
    name = StringField('Bean Name', validators=[DataRequired()])
    type = SelectField('Bean Type', choices=[(c, BEAN_TYPES[c]) for c in BEAN_TYPES],
                       coerce=int, validators=[DataRequired()])
    weight = IntegerField('Weight (grams)', validators=[DataRequired()])
    purchase_date = DateField('Purchase Date', validators=[DataRequired()], default=date.today())
    notes = TextAreaField('Notes', validators=[Optional()])


class BrewForm(Form):
    grind_size = SelectField('Grind Size', choices=[(g, GRIND_SIZES[g]) for g in GRIND_SIZES],
                             coerce=int, validators=[DataRequired()])
    bean_dose = IntegerField('Bean Weight (grams)', validators=[DataRequired()])
    water_dose = IntegerField('Water Volume (mL)', validators=[DataRequired()])
    extraction_time = IntegerField('Extraction Time (sec)', validators=[DataRequired()])
    brew_method = SelectField('Brew Method', choices=[(m, BREW_METHODS[m]) for m in BREW_METHODS],
                              coerce=int, validators=[DataRequired()])
    filter_type = SelectField('Filter Type', choices=[(f, FILTER_TYPES[f]) for f in FILTER_TYPES],
                              coerce=int, validators=[DataRequired()])
    brew_date = DateTimeField('Brew Date', validators=[DataRequired()], default=datetime.now())
    notes = TextAreaField('Notes', validators=[Optional()])
    roast_batch = SelectField('Roast Batch', coerce=int, validators=[Optional()])
    bean_id = SelectField('Bean', coerce=int, validators=[DataRequired()])