from flask import Flask, render_template, request, redirect, url_for
from Pagination.pagination import Pagination
from FileTransform.fileTransform import load_csv
from datetime import datetime
from src.area import areas_dict_test, areas_dict_ver1, areas_dict_ver2, k_to_e
from operator import itemgetter
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from utils import SECRET_KEY

#? 오늘이 무슨 요일인지 구하는 함수
def yoil():
    today = datetime.today().weekday()
    yoil_arr_k = ['월','화','수','목','금','토','일']
    yoil_arr_e = ['mon','tue','wed','thu','fri','sat','sun']
    return yoil_arr_k[today], yoil_arr_e[today]

#? 지금이 몇신지 구하는 함수 (ex. 18:30)
def time():
    now = datetime.now()
    return now.hour, now.minute

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simyasikdang.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

db = SQLAlchemy(app)

login_manager = LoginManager(app)  # 로그인 매니저 생성
login_manager.login_view = "login" # 로그인 페이지 URI 명시

class User(UserMixin, db.Model):
    id            = db.Column(db.Integer   , primary_key = True)
    userid        = db.Column(db.String(80), unique = True     , nullable = False)
    password_hash = db.Column(db.String(120)                    , nullable = False)
    email         = db.Column(db.String(80), unique = True     , nullable = True)
    User_R = db.relationship('UserLike')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class UserLike(db.Model):
    id            = db.Column(db.Integer    , primary_key = True)
    userid        = db.Column(db.String(64) , db.ForeignKey('user.id'))
    restaurantid  = db.Column(db.String(64) , db.ForeignKey('restaurants.id'))
    likesdate     = db.Column(db.String(64) , nullable = True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Restaurants(db.Model):
    id                   = db.Column(db.Integer, primary_key = True)
    create_time          = db.Column(db.String(64))
    area                 = db.Column(db.String(64))
    name                 = db.Column(db.String(64))
    type                 = db.Column(db.String(64))
    star_rating          = db.Column(db.String(64))
    review_sum           = db.Column(db.String(64))
    address              = db.Column(db.String(64))
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
    contact              = db.Column(db.String(64))
    restaurants_R = db.relationship('UserLike')

    def __repr__(self):
        return f'<Restaurants {self.area}, {self.name}, {self.type}, {self.star_rating}, {self.review_sum}, {self.contact}>'

@app.route('/')
def home():
    today_yoil_kor = yoil()[0]
    today_yoil_eng = yoil()[1]
    timenow = time()
    types = ['맥주,호프', '술집', '포장마차', '이자카야', '요리주점', '오뎅,꼬치', '전통,민속주점', '와인', '바(BAR)']
    null = '정보 없음'

    search      = request.args.get('search',      default='', type=str)
    area        = request.args.get('area',        default='', type=str)
    type        = request.args.get('type',        default='', type=str)
    timefromnow = request.args.get('timefromnow', default= 0, type=int)
    page        = request.args.get('page',        default= 1, type=int)

    #? default 창: 모든 지역의 데이터 다 가져오기
    areas = [] #? index.html option으로 사용
    for gu in areas_dict_test.keys():
        for dong in areas_dict_test[gu]:
            areas.append(dong)

    if area: # shopdata = load_csv(f"./csv/{k_to_e[area]}_processed.csv")
        restaurants = Restaurants.query.filter(Restaurants.area == k_to_e[area]).all()
    else:
        restaurants = Restaurants.query.all()

    shopdata = []
    for restaurant in restaurants:
        shopdata.append({'uuid'              : restaurant.id,
                        'create_time'        : restaurant.create_time,
                        'area'               : restaurant.area,
                        'name'               : restaurant.name,
                        'type'               : restaurant.type,
                        'star_rating'        : restaurant.star_rating,
                        'review_sum'         : restaurant.review_sum,
                        'address'            : restaurant.address,
                        'mon_opening_hours'  : restaurant.mon_opening_hours,
                        'mon_last_order_time': restaurant.mon_last_order_time,
                        'tue_opening_hours'  : restaurant.tue_opening_hours,
                        'tue_last_order_time': restaurant.tue_last_order_time,
                        'wed_opening_hours'  : restaurant.wed_opening_hours,
                        'wed_last_order_time': restaurant.wed_last_order_time,
                        'thu_opening_hours'  : restaurant.thu_opening_hours,
                        'thu_last_order_time': restaurant.thu_last_order_time,
                        'fri_opening_hours'  : restaurant.fri_opening_hours,
                        'fri_last_order_time': restaurant.fri_last_order_time,
                        'sat_opening_hours'  : restaurant.sat_opening_hours,
                        'sat_last_order_time': restaurant.sat_last_order_time,
                        'sun_opening_hours'  : restaurant.sun_opening_hours,
                        'sun_last_order_time': restaurant.sun_last_order_time,
                        'contact'            : restaurant.contact})

    if search:
        shopdata = [shop for shop in shopdata if search in shop['name']]
    if type:
        shopdata = [shop for shop in shopdata if type == shop['type']]
    if timefromnow:
        data = []
        for shop in shopdata:
            shop_time = shop[today_yoil_eng + "_opening_hours"]
            if shop_time in [null, '휴무', '정보없음', '정보 없음']:
                continue
            # shop_open_time  = int(shop_time[:2]) * 100 + int(shop_time[3:5])
            shop_close_time = int(shop_time[-5:-3]) * 100 + int(shop_time[-2:])
            timenow_int = timenow[0] * 100 + timenow[1]
            if timenow_int + timefromnow * 100 <= shop_close_time:
                data.append(shop)
        shopdata = data

    for shop in shopdata:
        shop_time = shop[f"{today_yoil_eng}_opening_hours"]
        
        if shop_time in [null, '휴무', '정보없음', '정보 없음']:
            shop['status'] = null
        else:
            shop_open_time  = int(shop_time[:2]) * 100 + int(shop_time[3:5])
            shop_close_time = int(shop_time[-5:-3]) * 100 + int(shop_time[-2:])
            timenow_int = timenow[0] * 100 + timenow[1]
            if timenow_int < shop_open_time:
                shop['status'] = '영업 전'
            elif timenow_int <= shop_close_time:
                shop['status'] = '영업 중'
            else:
                shop['status'] = '영업 종료'

            if shop_close_time >= 2400:
                shop[f"{today_yoil_eng}_opening_hours"] = shop_time + f'\n(~ 오전 {str(int(shop_time[-5:-3])-24)}:{shop_time[-2:]})'
            
    pagemaker = Pagination(shopdata, page)
    
    #? 기본 정렬: 별점 순 (얘보다 좀 더 빠름 <- shopdata = sorted(shopdata, key = lambda x: x['star_rating'], reverse=True) )
    shopdata = sorted(shopdata, key= itemgetter('star_rating'), reverse=True)

    print(current_user)

    return render_template("index.html", today_yoil_eng = today_yoil_eng, today_yoil_kor = today_yoil_kor, timenow = timenow, null = null,
                           areas = areas, types = types, search = search, area=area, type = type, timefromnow = timefromnow, 
                           shopdata = shopdata[pagemaker.start_index : pagemaker.end_index + 1],
                           page = page, total_page = pagemaker.total_page, 
                           pagination_start = pagemaker.pagination_start, 
                           pagination_end = pagemaker.pagination_end, 
                           move_page_front = pagemaker.move_page_front, 
                           move_page_back = pagemaker.move_page_back,
                           current_user = current_user)

@app.route('/register', methods = ["GET","POST"])
def register():
    if request.method == "POST":
        userid = request.form["id"]
        pw = request.form["pw"]
        pw_again = request.form["pw_again"]

        if pw != pw_again:
            print(f'비밀번호를 다시 입력해주세요')
            return redirect(url_for('register'))

        email = request.form["email"]

        existing_user_by_userid = User.query.filter_by(userid=userid).first()
        existing_user_by_email  = User.query.filter_by(email=email).first()
        if existing_user_by_userid:
            print('이미 있는 아이디입니다.')
            return redirect(url_for('register'))
        
        elif existing_user_by_email:
            print('이미 사용하는 이메일입니다.')
            return redirect(url_for('register'))

        new_user = User(userid = userid, email = email)
        new_user.set_password(pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        userid = request.form["id"]
        pw = request.form["pw"]
        user = User.query.filter_by(userid = userid).first()
        if user and user.check_password(pw):
            login_user(user) # 유저 로그인
            print(f'{current_user.userid}: 로그인에 성공했습니다.')
            return redirect(url_for('home'))
        else:
            print(f'로그인에 실패횄습니다.')
            return redirect(url_for('login'))
        
    # 3. 성공시 로그인 정보 저장하고 로그인 페이지로 이동
    #    실패시 오류 알려주기
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/singo')
def singo():
    area = request.args.get('area', default='', type=str)
    name = request.args.get('name', default='', type=str)
    return render_template('singo.html', area = area, name = name)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8888)