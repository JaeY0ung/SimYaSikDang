from flask import Flask, render_template, request
from Pagination.pagination import Pagination
from FileTransform.fileTransform import load_csv
from datetime import datetime
from src.area import areas_dict_test, areas_dict_ver1, areas_dict_ver2, k_to_e
from operator import itemgetter


#? 오늘이 무슨 요일인지 구하는 함수
def yoil():
    today = datetime.today().weekday()
    yoil_arr = ['월','화','수','목','금','토','일']
    return yoil_arr[today]

#? 지금이 몇신지 구하는 함수 (ex. 18:30)
def time():
    now = datetime.now()
    return now.hour, now.minute

null = '정보 없음'
types = ['맥주,호프', '술집', '포장마차', '이자카야', '요리주점', '오뎅,꼬치', '전통,민속주점', '와인', '바(BAR)']

application = Flask(__name__)
@application.route('/')
def home():
    today_yoil = yoil()
    timenow = time()

    page        = request.args.get('page',        default= 1, type=int)
    search      = request.args.get('search',      default='', type=str)
    area        = request.args.get('area',        default='', type=str)
    type        = request.args.get('type',        default='', type=str)
    timefromnow = request.args.get('timefromnow', default= 0, type=int)

    #? default 창: 모든 지역의 데이터 다 가져오기
    areas = [] #? index.html option으로 사용
    for gu in areas_dict_test.keys():
        for dong in areas_dict_test[gu]:
            areas.append(dong)

    if area:
        shopdata = load_csv(f"./csv/{k_to_e[area]}_processed.csv")

    if not area:
        shopdata = []
        for gu in areas_dict_test.keys():
            for dong in areas_dict_test[gu]:
                shopdata.extend(load_csv(f"./csv/{k_to_e[dong]}_processed.csv"))

    if search:
        shopdata = [shop for shop in shopdata if search in shop['name']]
    #? 필터 
    if type:
        shopdata = [shop for shop in shopdata if type == shop['type']]
    if timefromnow:
        data = []
        for shop in shopdata:
            shop_time = shop[today_yoil + "opening_hours"]
            if shop_time in [null, '휴무', '정보없음', '정보 없음']:
                continue
            # shop_open_time  = int(shop_time[:2]) * 100 + int(shop_time[3:5])
            shop_close_time = int(shop_time[-5:-3]) * 100 + int(shop_time[-2:])
            timenow_int = timenow[0] * 100 + timenow[1]
            if timenow_int + timefromnow * 100 <= shop_close_time:
                data.append(shop)
        shopdata = data

    for shop in shopdata:
        shop_time = shop[today_yoil + "opening_hours"]
        print(shop_time)
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
                shop[today_yoil + "opening_hours"] = shop_time + f'\n(~ 오전 {str(int(shop_time[-5:-3])-24)}:{shop_time[-2:]})'
            
    pagemaker = Pagination(shopdata, page)
    
    #? 기본 정렬: 별점 순
    #? 얘보다 좀 더 빠름 <- shopdata = sorted(shopdata, key = lambda x: x['star_rating'], reverse=True)
    shopdata = sorted(shopdata, key= itemgetter('star_rating'), reverse=True)

    return render_template("index.html", today_yoil = today_yoil, timenow = timenow, null = null,
                           areas=areas, types = types, search = search, area=area, type = type, timefromnow = timefromnow, 
                           shopdata = shopdata[pagemaker.start_index : pagemaker.end_index + 1],
                           page = page, total_page = pagemaker.total_page, 
                           pagination_start = pagemaker.pagination_start, 
                           pagination_end = pagemaker.pagination_end, 
                           move_page_front = pagemaker.move_page_front, 
                           move_page_back = pagemaker.move_page_back)


@application.route('/login')
def login():
    return render_template('login.html')

@application.route('/singo')
def singo():
    area = request.args.get('area', default='', type=str)
    name = request.args.get('name', default='', type=str)
    return render_template('singo.html', area = area, name = name)

if __name__ == '__main__':
    application.debug = True
    application.run(host="0.0.0.0", port=8888)