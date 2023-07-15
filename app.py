from flask import Flask, render_template, request
from Pagination.pagination import Pagination
from FileTransform.fileTransform import load_csv
from datetime import datetime
import src.seoul_area_data as seoul_area_data

# 오늘이 무슨 요일인지 구하는 함수
def yoil():
    today = datetime.today().weekday()
    yoil_arr = ['월','화','수','목','금','토','일']
    return yoil_arr[today]

# 지금이 몇신지 구하는 함수 (ex. 18:30)
def time():
    now = datetime.now()
    return now.hour, now.minute

null = '정보 없음'

areas_dict = seoul_area_data.areas_dict_test

areas = []
for gu in areas_dict.keys():
    for area in areas_dict[gu]:
        areas.append(area)

app = Flask(__name__)

@app.route('/')
def home():
    page = request.args.get('page', default=1, type=int)
    area = request.args.get('area', default='', type=str)
    if area:
        shopdata = load_csv(f"./csv/{area}_processed.csv")
    else:
        shopdata = load_csv("./csv/망원_processed.csv")
    today_yoil = yoil()
    timenow = time()
    
    for shop in shopdata:
        print(shop[f'{today_yoil}opening_hours'])

    pagemaker = Pagination()
    pagemaker.makepagination(shopdata, page)

    return render_template("home.html", today_yoil = today_yoil, timenow = timenow, 
                           areas=areas, area=area, null = null,
                           shopdata = shopdata[pagemaker.start_index : pagemaker.end_index + 1],
                           page = page, total_page = pagemaker.total_page, 
                           pagination_start = pagemaker.pagination_start, 
                           pagination_end = pagemaker.pagination_end, 
                           move_page_front = pagemaker.move_page_front, 
                           move_page_back = pagemaker.move_page_back)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)