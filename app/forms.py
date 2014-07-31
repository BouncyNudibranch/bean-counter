from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Optional
from app.models import BEAN_TYPES


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
    purchase_date = DateField('Purchase Date', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])