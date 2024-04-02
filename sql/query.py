from models import User, Place, UserLike
from flask_login import current_user
from sqlalchemy import func, or_, and_
import utils
from datetime import datetime, timedelta
from flask import current_app
from sqlalchemy.exc import OperationalError

time_now = utils.time()
today_yoil_kor = utils.yoil()[0]
today_yoil_eng = utils.yoil()[1]

class PlaceQuery():
    def __init__(self, search, address_gu, type, time_from_now, page, join_user=None):
        self.query = Place.query
        self.search = search
        self.address_gu = address_gu
        self.type = type
        self.time_from_now = time_from_now
        self.page = page
        if join_user:
            self.query = self.query.join(UserLike).filter(UserLike.userid == join_user.id)
        self.contain_search()
        self.contain_area()
        self.contain_type()
        self.order_by("star_rating") # 기본 정렬: 별점 순 
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
    def order_by(self, param):
        if param and param == "star_rating":
            self.query = self.query.order_by(Place.star_rating.desc())
    # def contain_page(self):
    #     if self.page:
    #         self.query = self.query.filter(Place.page == self.page)
    # def concat_address(self):
    #     self.result = self.result.with_entities(Place, func.concat(Place.address_si, ' ', Place.address_gu, ' ', Place.address_lo, ' ', Place.address_detail).label('full_address'))
    def filter_places_by_time_from_now():
        time_now = datetime.now()
        time_from_now = 2 # 예를 들어, 2시간 후
        try:
            session = current_app.db.session
            places = session.query(Place).all()
            filtered_places = []
            for place in places:
                opening_hours = getattr(place, f"{today_yoil_eng}_opening_hours")
                if opening_hours not in [None, '휴무', '정보없음', '정보 없음']:
                    open_time, close_time = opening_hours.split('-')

                    open_time = datetime.strptime(open_time, '%H:%M')
                    close_time = datetime.strptime(close_time, '%H:%M')
                    time_now_int = datetime.strptime(time_now.strftime('%H:%M'), '%H:%M').time()

                    # time_from_now_int = datetime.strptime(time_now.strftime('%H:%M') + f'{time_from_now} hour', '%H:%M%H:%M').time()
                    time_from_now_datetime = time_now + timedelta(hours=time_from_now)
                    time_from_now_int = datetime.strptime(time_from_now_datetime.strftime('%H:%M'), '%H:%M').time()

                    if (open_time <= time_now_int <= close_time 
                        or open_time <= time_now_int + timedelta(hours=24) <= close_time) \
                            and \
                            (open_time <= time_from_now_int <= close_time \
                            or open_time <= time_from_now_int + timedelta(hours=24) <= close_time):
                        filtered_places.append(place)
            return filtered_places
        finally:
            session.close()

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