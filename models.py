from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id            = db.Column(db.Integer   , primary_key = True)
    userid        = db.Column(db.String(80), unique = True, nullable = False)
    password_hash = db.Column(db.String(120),               nullable = False)
    email         = db.Column(db.String(80), unique = True)
    User_R        = db.relationship('UserLike')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class UserLike(db.Model):
    __tablename__ = 'userlike'
    id            = db.Column(db.Integer, primary_key = True)
    userid        = db.Column(db.String(64), db.ForeignKey('user.id'),  nullable = False)
    placeid       = db.Column(db.String(64), db.ForeignKey('place.id'), nullable = False)
    likesdate     = db.Column(db.String(64), nullable = True)


class Place(db.Model):
    __tablename__ = 'place'
    id                   = db.Column(db.Integer, primary_key = True)
    type_code            = db.Column(db.String(32), db.ForeignKey('typecode.id')) 
    name                 = db.Column(db.String(64), nullable=False)
    type                 = db.Column(db.String(64), nullable=False)
    star_rating          = db.Column(db.String(64))
    review_total         = db.Column(db.String(64))
    address_si           = db.Column(db.String(64), nullable=False)
    address_gu           = db.Column(db.String(64), nullable=False)
    address_lo           = db.Column(db.String(64), nullable=False)
    address_detail       = db.Column(db.String(64))
    contact              = db.Column(db.String(64))
    lat                  = db.Column(db.String(64))
    lng                  = db.Column(db.String(64))
    naver_place_id       = db.Column(db.String(64), nullable=False)
    place_url            = db.Column(db.String(64))
    road_url             = db.Column(db.String(64))
    mon_opening_hours    = db.Column(db.String(64))
    mon_last_order_time  = db.Column(db.String(64))
    tue_opening_hours    = db.Column(db.String(64))
    tue_last_order_time  = db.Column(db.String(64))
    wed_opening_hours    = db.Column(db.String(64))
    wed_last_order_time  = db.Column(db.String(64))
    thu_opening_hours    = db.Column(db.String(64))
    thu_last_order_time  = db.Column(db.String(64))
    fri_opening_hours    = db.Column(db.String(64))
    fri_last_order_time  = db.Column(db.String(64))
    sat_opening_hours    = db.Column(db.String(64))
    sat_last_order_time  = db.Column(db.String(64))
    sun_opening_hours    = db.Column(db.String(64))
    sun_last_order_time  = db.Column(db.String(64))
    created_at           = db.Column(db.String(64))
    place_R = db.relationship('UserLike')

    def __repr__(self):
        return f'<Place {self.address_si}, {self.name}, {self.type}, {self.star_rating}, {self.review_total}, {self.contact}>'


class TypeCode(db.Model):
    __tablename__ = 'typecode'
    id   = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(64), unique = True)
    code = db.Column(db.String(64), unique = True)

    def __repr__(self):
        return f'<TypeCode {self.id}, {self.type}, {self.code}>'