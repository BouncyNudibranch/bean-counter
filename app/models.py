from pbkdf2 import crypt

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def verify_password(self, password):
        return self.password == crypt(password, self.password)

    @staticmethod
    def hash_password(password):
        return crypt(password)

    @staticmethod
    def add_user(user, commit=True):
        db.session.add(user)
        if commit:
            db.session.commit()


class Brew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grind_size = db.Column(db.SmallInteger)
    bean_dose = db.Column(db.Integer)
    water_dose = db.Column(db.Integer)
    extraction_time = db.Column(db.Integer)
    brew_method = db.Column(db.SmallInteger)
    filter_type = db.Column(db.SmallInteger)
    brew_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    bean_id = None
    user_id = None
    roast_id = None


class Roast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bean_dose = db.Column(db.Integer)
    drop_temp = db.Column(db.SmallInteger)
    dry_end_time = db.Column(db.Integer)
    dry_end_temp = db.Column(db.SmallInteger)
    fc_begin_time = db.Column(db.Integer)
    fc_begin_temp = db.Column(db.SmallInteger)
    fc_end_time = db.Column(db.Integer)
    fc_end_temp = db.Column(db.SmallInteger)
    sc_begin_time = db.Column(db.Integer)
    sc_begin_temp = db.Column(db.SmallInteger)
    sc_end_time = db.Column(db.Integer)
    sc_end_temp = db.Column(db.SmallInteger)
    end_time = db.Column(db.Integer)
    end_temp = db.Column(db.SmallInteger)
    end_weight = db.Column(db.SmallInteger)
    roaster_machine = db.Column(db.SmallInteger)
    roast_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    bean_id = None
    user_id = None


class Bean(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    weight = db.Column(db.SmallInteger)
    purchase_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    user_id = None