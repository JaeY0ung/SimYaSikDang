from flask import Flask, render_template, request
from Pagination.pagination import Pagination
from FileTransform.fileTransform import load_csv
from datetime import datetime
import src.seoul_area_data as seoul_area_data
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
areas_dict = seoul_area_data.areas_dict_test
types = ['맥주,호프', '술집', '포장마차', '이자카야', '요리주점', '오뎅,꼬치', '전통,민속주점', '와인', '바(BAR)']

areas = []
for gu in areas_dict.keys():
    for area in areas_dict[gu]:
        areas.append(area)

app = Flask(__name__)
@app.route('/')
def home():
    today_yoil = yoil()
    timenow = time()
    #? default 창
    shopdata = load_csv("./csv/망원_processed.csv")

    page = request.args.get('page', default=1, type=int)
    area = request.args.get('area', default='', type=str)
    type = request.args.get('type', default='', type=str)
    timefromnow = request.args.get('timefromnow', default=0, type=int)

    for shop in shopdata:
        shop_time = shop[today_yoil + "opening_hours"]
        if shop_time in [null, '휴무']:
            shop['status'] = null
        else:
            print(f'현재 시간: {timenow}')
            shop_open_time  = int(shop_time[:2]) * 100 + int(shop_time[3:5])
            shop_close_time = int(shop_time[-5:-3]) * 100 + int(shop_time[-2:])
            timenow_int = timenow[0] * 100 + timenow[1]
            if timenow_int < shop_open_time:
                shop['status'] = '영업 전'
            elif timenow_int <= shop_close_time:
                shop['status'] = '영업 중'
            else:
                shop['status'] = '영업 종료'
    
    #? 필터 
    if area:
        shopdata = load_csv(f"./csv/{area}_processed.csv")
    if type:
        shopdata = [shop for shop in shopdata if type == shop['type']]
    if timefromnow:
        data = []
        for shop in shopdata:
            shop_time = shop[today_yoil + "opening_hours"]
            if shop_time in [null, '휴무']:
                continue
            shop_open_time  = int(shop_time[:2]) * 100 + int(shop_time[3:5])
            shop_close_time = int(shop_time[-5:-3]) * 100 + int(shop_time[-2:])
            timenow_int = timenow[0] * 100 + timenow[1]
            if timenow_int + timefromnow <= shop_close_time:
                data.append(shop)
        shopdata = data
            
    pagemaker = Pagination()
    pagemaker.makepagination(shopdata, page)
    print('before', shopdata)
    #? 기본 정렬: 별점 순
    #? 얘보다 좀 더 빠름 <- shopdata = sorted(shopdata, key = lambda x: x['star_rating'], reverse=True)
    shopdata = sorted(shopdata, key= itemgetter('star_rating'), reverse=True)

    return render_template("home.html", today_yoil = today_yoil, timenow = timenow, null = null,
                           areas=areas, area=area, types = types, type = type, timefromnow = timefromnow, 
                           shopdata = shopdata[pagemaker.start_index : pagemaker.end_index + 1],
                           page = page, total_page = pagemaker.total_page, 
                           pagination_start = pagemaker.pagination_start, 
                           pagination_end = pagemaker.pagination_end, 
                           move_page_front = pagemaker.move_page_front, 
                           move_page_back = pagemaker.move_page_back)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)