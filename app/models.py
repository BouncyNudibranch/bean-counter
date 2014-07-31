from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))


class Brew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grind_size = db.Column(db.SmallInteger)
    bean_dose = db.Column(db.Integer)
    water_dose = db.Column(db.Integer)
    extraction_time = db.Column(db.Integer)
    brew_method = db.Column(db.SmallInteger)
    filter_type = db.Column(db.SmallInteger)
