from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from pagination import Pagination
from crawler.fileTransform import load_csv, naver_place_csv_to_db
from datetime import datetime
from operator import itemgetter
from models import db, User, UserLike, Place, TypeCode
from crawler.constant import dict_area_gu_to_dong, dict_area_kor_to_eng, dict_searchtype_to_code
from crawler.constant import SECRET_KEY, NULL, dict_area_kor_to_eng
from crawler.Data_Crawl_and_Process import Data_Crawl_and_Process

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simyasikdang.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

login_manager = LoginManager(app)  #! 로그인 매니저 생성
login_manager.login_view = "login" #! 로그인 페이지 URI 명시
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db.init_app(app)

# Migrate 설정
migrate = Migrate(app, db)

def yoil(): #! 오늘이 무슨 요일인지 구하는 함수 return (한글 요일, 영어 요일)
    today = datetime.today().weekday()
    yoil_arr_kor = ['월','화','수','목','금','토','일']
    yoil_arr_eng = ['mon','tue','wed','thu','fri','sat','sun']
    return yoil_arr_kor[today], yoil_arr_eng[today]

def time(): #! 지금이 몇신지 구하는 함수 return (시간, 분)
    now = datetime.now()
    return now.hour, now.minute

@app.route('/')
def home():
    today_yoil_kor = yoil()[0]
    today_yoil_eng = yoil()[1]
    timenow        = time()
    types          = ['맥주,호프', '술집', '포장마차', '이자카야', '요리주점', '오뎅,꼬치', '전통,민속주점', '와인', '바(BAR)']

    search      = request.args.get('search',      default='', type=str)
    area        = request.args.get('area',        default='', type=str)
    type        = request.args.get('type',        default='', type=str)
    timefromnow = request.args.get('timefromnow', default= 0, type=int)
    page        = request.args.get('page',        default= 1, type=int)

    #? default 창: 모든 지역의 데이터 다 가져오기
    areas = [] #? index.html option으로 사용
    for dong in dict_area_kor_to_eng:
        areas.append(dong)

    if area: #? shopdata = load_csv(f"./csv/{area_k_to_e[area]}_processed.csv")
        places = Place.query.filter(Place.area == dict_area_kor_to_eng[area]).all()
    else:
        places = Place.query.all()

    shopdata = []
    for place in places:
        shopdata.append({
                        'uuid'               : place.id,
                        'type_code'          : place.type_code,
                        'name'               : place.name,
                        'type'               : place.type,
                        'star_rating'        : place.star_rating,
                        'address_si'         : place.address_si,
                        'address_gu'         : place.address_gu,
                        'address_lo'         : place.address_lo,
                        'address_detail'     : place.address_detail,
                        'contact'            : place.contact,
                        'lat'                : place.lat,
                        'lng'                : place.lng,
                        'naver_place_id'     : place.naver_place_id,
                        'place_url'          : place.place_url,
                        'road_url'           : place.road_url,
                        'review_total'       : place.review_total,
                        'mon_opening_hours'  : place.mon_opening_hours,
                        'mon_last_order_time': place.mon_last_order_time,
                        'tue_opening_hours'  : place.tue_opening_hours,
                        'tue_last_order_time': place.tue_last_order_time,
                        'wed_opening_hours'  : place.wed_opening_hours,
                        'wed_last_order_time': place.wed_last_order_time,
                        'thu_opening_hours'  : place.thu_opening_hours,
                        'thu_last_order_time': place.thu_last_order_time,
                        'fri_opening_hours'  : place.fri_opening_hours,
                        'fri_last_order_time': place.fri_last_order_time,
                        'sat_opening_hours'  : place.sat_opening_hours,
                        'sat_last_order_time': place.sat_last_order_time,
                        'sun_opening_hours'  : place.sun_opening_hours,
                        'sun_last_order_time': place.sun_last_order_time,
                        'created_at'         : place.created_at,
                        })

    if search:
        shopdata = [shop for shop in shopdata if search in shop['name']]
    if type:
        shopdata = [shop for shop in shopdata if type == shop['type']]
    if timefromnow:
        data = []
        for shop in shopdata:
            shop_time = shop[today_yoil_eng + "_opening_hours"]
            if shop_time in [NULL, '휴무', '정보없음', '정보 없음']:
                continue
            #? shop_open_time  = int(shop_time[:2]) * 100 + int(shop_time[3:5])
            shop_close_time = int(shop_time[-5:-3]) * 100 + int(shop_time[-2:])
            timenow_int = timenow[0] * 100 + timenow[1]
            if timenow_int + timefromnow * 100 <= shop_close_time:
                data.append(shop)
        shopdata = data

    for shop in shopdata:
        shop_time = shop[f"{today_yoil_eng}_opening_hours"]
        
        if shop_time in [NULL, '휴무', '정보없음', '정보 없음']:
            shop['status'] = NULL
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

    return render_template("index.html", today_yoil_eng = today_yoil_eng, today_yoil_kor = today_yoil_kor, timenow = timenow, NULL = NULL,
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
        
    #? 3. 성공시 로그인 정보 저장하고 로그인 페이지로 이동
    #?    실패시 오류 알려주기
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/singo')
@login_required
def singo():
    area = request.args.get('area', default='', type=str)
    name = request.args.get('name', default='', type=str)
    return render_template('singo.html', area = area, name = name)


@app.route('/data-process')
@login_required
def data_process():
    if current_user.userid == "admin":
        return render_template('data_process.html')
    return render_template('404.html')


@app.route('/crawl')
@login_required
def crawl():
    if current_user.userid == "admin":
        data_processor = Data_Crawl_and_Process()
        data_processor.get_all_area()
        return redirect(url_for('data_process'))
    return render_template('404.html')


@app.route('/save-data-to-db')
@login_required
def save_data_to_db():
    if current_user.userid == "admin":
        #! db에 저장 코드
        for dongs in dict_area_gu_to_dong.values():
            for dong in dongs:
                for searchtype, code in dict_searchtype_to_code.items():
                    try:
                        naver_place_csv_to_db(dong, code)
                        print(f'{dong} {searchtype} 데이터 저장 완료')
                    except:
                        print(f'{dong} {searchtype} 데이터 저장 실패')
        return redirect(url_for('data_process'))
    return render_template('404.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8000) # app.run(host="0.0.0.0", port=8000)