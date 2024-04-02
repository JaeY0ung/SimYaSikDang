from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id            = db.Column(db.Integer, primary_key = True)
    username      = db.Column(db.String(64), unique = True, nullable = False) # 아이디
    password_hash = db.Column(db.String(128),               nullable = False) # 비밀번호 
    nickname      = db.Column(db.String(64)) # TODO : unique = True 향후 추가할 것
    contact       = db.Column(db.String(64))
    email         = db.Column(db.String(64), unique = True)
    name          = db.Column(db.String(64))
    user_like     = db.relationship('UserLike', backref=db.backref('user')) #? 잘 모름
    singo         = db.relationship('Singo', backref=db.backref('user')) #? 잘 모름

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Place(db.Model):
    __tablename__        = 'place'
    id                   = db.Column(db.Integer, primary_key = True)
    uuid                 = db.Column(db.String(64), nullable=True)   # uri에 쓸거 (스크랩핑에 따른 트래픽 방지를 위해 난수)
    type_code            = db.Column(db.Integer, db.ForeignKey('typecode.id', ondelete='CASCADE')) 
    name                 = db.Column(db.String(64), nullable=False)
    type                 = db.Column(db.String(64), nullable=False)
    star_rating          = db.Column(db.String(64)) # TODO : float 타입으로 바꾸기
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
    naver_road_url       = db.Column(db.String(64))
    kakao_road_url       = db.Column(db.String(64))
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
    user_like            = db.relationship('UserLike', backref=db.backref('place')) #? 잘 모름
    singo                = db.relationship('Singo', backref=db.backref('place')) #? 잘 모름

    def __repr__(self):
        return f'<Place({self.id}) 지역:{self.address_si}, 이름:{self.name}, 가게종류:{self.type}, 별점:{self.star_rating}, 리뷰수:{self.review_total}, 연락처:{self.contact}>'
    
class UserLike(db.Model):
    __tablename__ = 'userlike'
    id            = db.Column(db.Integer, primary_key = True)
    userid        = db.Column(db.Integer, db.ForeignKey('user.id',  ondelete='CASCADE'), nullable = False)
    placeid       = db.Column(db.Integer, db.ForeignKey('place.id', ondelete='CASCADE'), nullable = False)
    likedate      = db.Column(db.String(64), nullable = False)

    def __repr__(self):
        return f'<UserLike({self.id}) user:{self.userid}  place:{self.placeid}>'

class TypeCode(db.Model):
    __tablename__ = 'typecode'
    id   = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(64), unique = True)
    code = db.Column(db.String(64), unique = True)

    def __repr__(self):
        return f'<TypeCode({self.id}) type:{self.type}, code:{self.code}>'
    
class Singo(db.Model):
    __tablename__ = 'singo'
    id            = db.Column(db.Integer, primary_key = True)
    userid        = db.Column(db.Integer, db.ForeignKey('user.id',  ondelete='CASCADE'), nullable = True) # TODO : cascade 옵션 바꿔야 함
    placeid       = db.Column(db.Integer, db.ForeignKey('place.id', ondelete='CASCADE'), nullable = False)
    contact       = db.Column(db.String(64))
    email         = db.Column(db.String(64))

    def __repr__(self):
        return f'<Singo({self.id}) user:{self.userid}, place:{self.placeid}>'