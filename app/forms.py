from datetime import date, datetime
from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, SelectField, DateField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, EqualTo, Optional, NumberRange
from app.models import BEAN_TYPES, GRIND_SIZES, BREW_METHODS, FILTER_TYPES, ROASTER_MACHINES


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
                       coerce=int, validators=[NumberRange(min=0)])
    weight = IntegerField('Weight (grams)', validators=[NumberRange(min=0)])
    purchase_date = DateField('Purchase Date', validators=[DataRequired()], default=date.today())
    notes = TextAreaField('Notes', validators=[Optional()])


class BrewForm(Form):
    grind_size = SelectField('Grind Size', choices=[(g, GRIND_SIZES[g]) for g in GRIND_SIZES],
                             coerce=int, validators=[NumberRange(min=0)])
    bean_dose = IntegerField('Bean Weight (grams)', validators=[NumberRange(min=0)])
    water_dose = IntegerField('Water Volume (mL)', validators=[NumberRange(min=0)])
    extraction_time = IntegerField('Extraction Time (sec)', validators=[NumberRange(min=0)])
    brew_method = SelectField('Brew Method', choices=[(m, BREW_METHODS[m]) for m in BREW_METHODS],
                              coerce=int, validators=[NumberRange(min=0)])
    filter_type = SelectField('Filter Type', choices=[(f, FILTER_TYPES[f]) for f in FILTER_TYPES],
                              coerce=int, validators=[NumberRange(min=0)])
    brew_date = DateTimeField('Brew Date', validators=[DataRequired()], default=datetime.now())
    notes = TextAreaField('Notes', validators=[Optional()])
    roast_batch = SelectField('Roast Batch', coerce=int, validators=[Optional()])
    bean_id = SelectField('Bean', coerce=int, validators=[NumberRange(min=0)])


class RoastForm(Form):
    bean_dose = IntegerField('Bean Weight (grams)', validators=[NumberRange(min=0)])
    drop_temp = IntegerField('Drop Temp (F)', validators=[NumberRange(min=0)])
    dry_end_time = IntegerField('Drying Phase End Time (sec)', validators=[NumberRange(min=0)])
    dry_end_temp = IntegerField('Drying Phase End Temp (F)', validators=[NumberRange(min=0)])
    fc_begin_time = IntegerField('First Crack Begin Time (sec)', validators=[NumberRange(min=0)])
    fc_begin_temp = IntegerField('First Crack Begin Temp (F)', validators=[NumberRange(min=0)])
    fc_end_time = IntegerField('First Crack End Time (sec)', validators=[NumberRange(min=0)])
    fc_end_temp = IntegerField('First Crack End Temp (F)', validators=[NumberRange(min=0)])
    sc_begin_time = IntegerField('Second Crack Begin Time (sec)', validators=[NumberRange(min=0)])
    sc_begin_temp = IntegerField('Second Crack Begin Temp (F)', validators=[NumberRange(min=0)])
    sc_end_time = IntegerField('Second Crack End Time (sec)', validators=[NumberRange(min=0)])
    sc_end_temp = IntegerField('Second Crack End Temp (F)', validators=[NumberRange(min=0)])
    end_time = IntegerField('End Time (sec)', validators=[NumberRange(min=0)])
    end_temp = IntegerField('End Temp (F)', validators=[NumberRange(min=0)])
    end_weight = IntegerField('End Weight (grams)', validators=[NumberRange(min=0)])
    roaster_machine = SelectField('Roaster', choices=[(r, ROASTER_MACHINES[r]) for r in ROASTER_MACHINES],
                                  coerce=int, validators=[NumberRange(min=0)])
    roast_date = DateTimeField('Roast Date', validators=[DataRequired()], default=datetime.now())
    notes = TextAreaField('Notes', validators=[Optional()])
    bean_id = SelectField('Bean', coerce=int, validators=[NumberRange(min=0)])