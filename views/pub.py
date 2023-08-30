from flask import Blueprint, render_template, request, session
from flask_login import current_user
from pagination import Pagination
from crawler.constant import NULL
from models import User, UserLike, Place, TypeCode
from secret import KAKAO_JAVASCRIPT_KEY
from datetime import datetime
from operator import itemgetter
from datetime import datetime

bp = Blueprint('pub', __name__, url_prefix = '/pub')

def yoil(): #! 오늘이 무슨 요일인지 구하는 함수 return (한글 요일, 영어 요일)
    today = datetime.today().weekday()
    hour_now = datetime.now().hour
    yoil_arr_kor = ['월','화','수','목','금','토','일']
    yoil_arr_eng = ['mon','tue','wed','thu','fri','sat','sun']
    if hour_now <= 10: #! 술집이므로 오전 10:59까지는 전날 시간으로 계산하는 것이 맞다고 생각!
        return yoil_arr_kor[today], yoil_arr_eng[today-1]
    return yoil_arr_kor[today], yoil_arr_eng[today]

def time(): #! 지금이 몇신지 구하는 함수 return (시간, 분)
    now = datetime.now()
    return now.hour, now.minute

@bp.route('')
def index():
    today_yoil_kor = yoil()[0]
    today_yoil_eng = yoil()[1]
    timenow        = time()

    search      = request.args.get('search',      default='', type=str)
    area        = request.args.get('area',        default='', type=str)
    type        = request.args.get('type',        default='', type=str)
    timefromnow = request.args.get('timefromnow', default= 0, type=int)
    page        = request.args.get('page',        default= 1, type=int)

    place_type_obj = TypeCode.query.filter_by(type = "술집").first()
    #! area 필터에 사용할 지역들(구) 가져오기
    areas = [i[0] for i in Place.query.with_entities(Place.address_gu).distinct().all()]
    #! type 필터에 사용할 술집의 type들만 가져오기
    types = [i[0] for i in Place.query.filter_by(type_code = place_type_obj.id).with_entities(Place.type).distinct().all()]

    if area: # 지역 필터 사용 시
        places = Place.query.filter_by(address_gu = area,
                                       type_code = place_type_obj.id).all()
    else: # 지역 필터가 전체일 시
        places = Place.query.filter_by(type_code = place_type_obj.id).all()

    place_data = []
    for place in places:
        try: #! 로그인한 유저가 있으면
            is_like = User.query.join(UserLike)\
                            .filter(UserLike.placeid == place.id, 
                                    UserLike.userid == current_user.id).first()
        except AttributeError: #! 로그인한 유저가 없으면
            is_like = None

        place_data.append({
                        'is_like'            : is_like,
                        'id'                 : place.id,
                        'uuid'               : place.uuid,
                        'type_code'          : place.type_code,
                        'name'               : place.name,
                        'type'               : place.type,
                        'star_rating'        : place.star_rating,
                        'address_si'         : place.address_si,
                        'address_gu'         : place.address_gu,
                        'address_lo'         : place.address_lo,
                        'address_detail'     : place.address_detail,
                        'address'            : f'{place.address_si} {place.address_gu} {place.address_lo} {place.address_detail}',
                        'contact'            : place.contact,
                        'lat'                : place.lat,
                        'lng'                : place.lng,
                        'naver_place_id'     : place.naver_place_id,
                        'place_url'          : place.place_url,
                        'naver_road_url'     : place.naver_road_url,
                        'kakao_road_url'     : place.kakao_road_url,
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

    if search: #! 검색명 입력 시 가게명으로 검색
        place_data = [shop for shop in place_data if search in shop['name']]

    if type: #! 장소 타입 필터 옵션 선택 시 
        place_data = [shop for shop in place_data if type == shop['type']]

    if timefromnow: #! 시간 필터 클릭 시 추가
        data = []
        for shop in place_data:
            shop_time = shop[today_yoil_eng + "_opening_hours"]
            if shop_time in [NULL, '휴무', '정보없음', '정보 없음']:
                continue
            shop_open_time  = int(shop_time[:2]) * 100 + int(shop_time[3:5])
            shop_close_time = int(shop_time[-5:-3]) * 100 + int(shop_time[-2:])
            timenow_int     = timenow[0] * 100 + timenow[1]
            #! 지금도 열고, 이따도 여는 곳들만 보여주기
            if (shop_open_time <= timenow_int <= shop_close_time\
                or shop_open_time <= timenow_int + 2400 <= shop_close_time)\
                and\
                (shop_open_time <= timenow_int + timefromnow * 100 <= shop_close_time\
                or shop_open_time <= timenow_int + timefromnow * 100 + 2400 <= shop_close_time):
                data.append(shop)
        place_data = data

    for shop in place_data:
        shop_time = shop[f"{today_yoil_eng}_opening_hours"]
        
        if shop_time in [NULL, '정보없음', '정보 없음']:
            shop['status'] = NULL
        elif shop_time in ['휴무']:
            shop['status'] = '휴무'
        else:
            shop_open_time  = int(shop_time[:2]) * 100 + int(shop_time[3:5])
            shop_close_time = int(shop_time[-5:-3]) * 100 + int(shop_time[-2:])
            timenow_int     = timenow[0] * 100 + timenow[1]
            # print(f'여는 시간: {shop_open_time}\n현재 시간: {timenow_int}\n닫는 시간: {shop_close_time}\nㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
          
            if shop_open_time <= timenow_int <= shop_close_time:
                shop['status'] = 'open'  # '영업 중'
            else:
                shop['status'] = 'close' # '영업 종료'

            if shop_close_time >= 2400:
                shop[f"{today_yoil_eng}_opening_hours"] = shop_time[:5] + f'-{str(int(shop_time[-5:-3]) - 24):>02s}:{shop_time[-2:]}'
                if shop_open_time <= timenow_int + 2400 <= shop_close_time:
                    shop['status'] = 'open' #'영업 중'
            
    pagemaker = Pagination(place_data, page)
    
    #? 기본 정렬: 별점 순 (얘보다 좀 더 빠름 <- place_data = sorted(place_data, key = lambda x: x['star_rating'], reverse=True) )
    place_data = sorted(place_data, key=itemgetter('star_rating'), reverse=True)

    print(current_user)

    return render_template("pub.html", today_yoil_eng = today_yoil_eng, today_yoil_kor = today_yoil_kor, timenow = timenow, NULL = NULL,
                           areas = areas, types = types, search = search, area=area, type = type, timefromnow = timefromnow, 
                           place_data = place_data[pagemaker.start_index : pagemaker.end_index + 1],
                           page = page, total_page = pagemaker.total_page, 
                           pagination_start = pagemaker.pagination_start, 
                           pagination_end = pagemaker.pagination_end, 
                           move_page_front = pagemaker.move_page_front, 
                           move_page_back = pagemaker.move_page_back,
                           current_user = current_user,
                           KAKAO_JAVASCRIPT_KEY = KAKAO_JAVASCRIPT_KEY)