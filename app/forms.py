from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Optional


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
    type = SelectField('Bean Type', choices=[
        (1, 'Green'),
        (2, 'Roasted'),
        (3, 'Pre-ground')
    ], coerce=int, validators=[DataRequired()])
    weight = IntegerField('Weight (grams)', validators=[DataRequired()])
    purchase_date = DateField('Purchase Date', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])