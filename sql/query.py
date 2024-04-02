from models import User, Place, UserLike
from flask_login import current_user
from sqlalchemy import func

class PlaceQuery():
    def __init__(self, search, address_gu, type, time_from_now, page):
        self.query = Place.query
        self.search = search
        self.address_gu = address_gu
        self.type = type
        self.time_from_now = time_from_now
        self.page = page

        self.contain_search()
        self.contain_area()
        self.contain_type()
        # self.contain_page()
        # self.contain_time_from_now()
        # self.concat_address()
        # self.contain_like()

    def contain_search(self):
        if self.search:
            self.query = self.query.filter(Place.name.like(f"%{self.search}%"))
    def contain_area(self):
        if self.address_gu:
            self.query = self.query.filter(Place.address_gu == self.address_gu)
    def contain_type(self):
        if self.type:
            self.query = self.query.filter(Place.type == self.type)
    # def contain_page(self):
    #     if self.page:
    #         self.query = self.query.filter(Place.page == self.page)
    # def concat_address(self):
    #     self.result = self.result.with_entities(Place, func.concat(Place.address_si, ' ', Place.address_gu, ' ', Place.address_lo, ' ', Place.address_detail).label('full_address'))
    def get_result(self):
        return self.query.all()
    
class UserQuery():
    def __init__(self, current_user):
        self.query = UserLike.query
        self.current_user = current_user
        self.contain_current_user()

    def contain_current_user(self):
        if self.current_user.is_authenticated: # TODO : is_authenticated 빼도 되는지
            self.query = self.query.filter_by(userid=current_user.id).with_entities(UserLike.placeid)
    # def contain_like(self):
    #     if current_user.is_authenticated: #! 로그인한 유저가 있으면
    #         is_like = User.query.join(UserLike).filter(UserLike.placeid == place.id, UserLike.userid == current_user.id).first()
    def get_result(self):
        return self.query.all()