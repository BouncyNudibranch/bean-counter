"""
Bean Counter - Track Your Coffee!
Copyright (C) 2014  BouncyNudibranch (bouncynudibranch@gmail.com)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from pbkdf2 import crypt

from app import db


BEAN_TYPES = {
    1: 'Green',
    2: 'Roasted',
    3: 'Pre-ground'
}
GRIND_SIZES = {
    1: 'Extra Coarse',
    2: 'Coarse',
    3: 'Medium-Coarse',
    4: 'Medium',
    5: 'Medium-Fine',
    6: 'Fine',
    7: 'Extra Fine'
}
FILTER_TYPES = {
    1: 'None',
    2: 'Paper',
    3: 'Stainless Steel'
}
BREW_METHODS = {
    0: 'Other',
    1: 'Aeropress',
    2: 'Chemex',
    3: 'Clever',
    4: 'Cold Brew',
    5: 'Pour Over',
    6: 'Press',
    7: 'Siphon/Vac Pot',
    8: 'Stove Top',
    9: 'Turkish'
}
ROASTER_MACHINES = {
    0: 'Other',
    1: 'FreshRoast SR300',
    2: 'FreshRoast SR500',
    3: 'FreshRoast SR700',
    4: 'Behmor 1600',
    5: 'Behmor 1600 Plus',
    6: 'Popcorn Air Popper',
    7: 'Whirley Pop',
    8: 'Cast Iron Skillet',
    9: 'Heat Gun'
}


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

    bean_id = db.Column(db.Integer, db.ForeignKey('bean.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    roast_id = db.Column(db.Integer, db.ForeignKey('roast.id'), default=None)

    def brew_method_str(self):
        return BREW_METHODS[self.brew_method]

    def filter_type_str(self):
        return FILTER_TYPES[self.filter_type]

    def grind_size_str(self):
        return GRIND_SIZES[self.grind_size]

    def remove_brew(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    @staticmethod
    def add_brew(brew, commit=True):
        db.session.add(brew)
        if commit:
            db.session.commit()


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

    bean_id = db.Column(db.Integer, db.ForeignKey('bean.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    brews = db.relationship('Brew', backref='roast', lazy='dynamic')
    cuppings = db.relationship('Cupping', backref='roast', lazy='dynamic')

    def roaster_machine_str(self):
        return ROASTER_MACHINES[self.roaster_machine]

    def remove_roast(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    @staticmethod
    def add_roast(roast, commit=True):
        db.session.add(roast)
        if commit:
            db.session.commit()


class Bean(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    bean_type = db.Column(db.SmallInteger)
    weight = db.Column(db.SmallInteger)
    purchase_date = db.Column(db.Date)
    notes = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    brews = db.relationship('Brew', backref='bean', lazy='dynamic')
    roasts = db.relationship('Roast', backref='bean', lazy='dynamic')

    def bean_type_str(self):
        return BEAN_TYPES[self.bean_type]

    def remove_bean(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    def get_aggregate_roast_stats(self):
        q = db.session.query(
            Roast,
            db.func.min(db.func.nullif(Roast.dry_end_time, 0)),
            db.func.max(db.func.nullif(Roast.dry_end_time, 0)),
            db.func.min(db.func.nullif(Roast.dry_end_temp, 0)),
            db.func.max(db.func.nullif(Roast.dry_end_temp, 0)),
            db.func.min(db.func.nullif(Roast.fc_begin_time, 0)),
            db.func.max(db.func.nullif(Roast.fc_begin_time, 0)),
            db.func.min(db.func.nullif(Roast.fc_begin_temp, 0)),
            db.func.max(db.func.nullif(Roast.fc_begin_temp, 0)),
            db.func.min(db.func.nullif(Roast.fc_end_time, 0)),
            db.func.max(db.func.nullif(Roast.fc_end_time, 0)),
            db.func.min(db.func.nullif(Roast.fc_end_temp, 0)),
            db.func.max(db.func.nullif(Roast.fc_end_temp, 0)),
            db.func.min(db.func.nullif(Roast.sc_begin_time, 0)),
            db.func.max(db.func.nullif(Roast.sc_begin_time, 0)),
            db.func.min(db.func.nullif(Roast.sc_begin_temp, 0)),
            db.func.max(db.func.nullif(Roast.sc_begin_temp, 0)),
            db.func.min(db.func.nullif(Roast.sc_end_time, 0)),
            db.func.max(db.func.nullif(Roast.sc_end_time, 0)),
            db.func.min(db.func.nullif(Roast.sc_end_temp, 0)),
            db.func.max(db.func.nullif(Roast.sc_end_temp, 0)),
            db.func.min(db.func.nullif(Roast.end_time, 0)),
            db.func.max(db.func.nullif(Roast.end_time, 0)),
            db.func.min(db.func.nullif(Roast.end_temp, 0)),
            db.func.max(db.func.nullif(Roast.end_temp, 0)),
            db.func.min(db.func.nullif(Roast.drop_temp, 0)),
            db.func.max(db.func.nullif(Roast.drop_temp, 0))
        )
        q = q.filter(Roast.bean_id == self.id).group_by(Roast.roaster_machine).all()
        return q

    @staticmethod
    def add_bean(bean, commit=True):
        db.session.add(bean)
        if commit:
            db.session.commit()


class Cupping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    aroma_notes = db.Column(db.Text)
    acidity_notes = db.Column(db.Text)
    flavour_notes = db.Column(db.Text)
    mouthfeel_notes = db.Column(db.Text)
    aftertaste_notes = db.Column(db.Text)
    overall_notes = db.Column(db.Text)
    extra_notes = db.Column(db.Text)

    roast_id = db.Column(db.Integer, db.ForeignKey('roast.id'))

    def remove_cupping(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    @staticmethod
    def add_cupping(cupping, commit=True):
        db.session.add(cupping)
        if commit:
            db.session.commit()