from flask import Blueprint, render_template, request
from flask_login import current_user
from pagination import Pagination
from models import User, UserLike, Place, TypeCode
from secret import KAKAO_JAVASCRIPT_KEY
from operator import itemgetter
import utils
from constant import NULL
from sql.query import PlaceQuery, UserQuery
from sqlalchemy import func

bp = Blueprint('pub', __name__, url_prefix='/pub')

time_now = utils.time()
today_yoil_kor = utils.yoil()[0]
today_yoil_eng = utils.yoil()[1]

@bp.route('')
def index():
    print(f"[pub.index] username: {current_user.nickname}")

    filter_selected = {
        'search': request.args.get('search', default='', type=str),
        'area_gu': request.args.get('area', default='', type=str),
        'type': request.args.get('type', default='', type=str),
        'time_from_now': request.args.get('timefromnow', default=0, type=int),
        'page': request.args.get('page', default=1, type=int)
    }

    areas = [place[0] for place in Place.query.with_entities(Place.address_gu).distinct().all()]
    place_type_code_id = TypeCode.query.filter(TypeCode.type=="술집").first().id
    place_types = [place[0] for place in Place.query.filter(Place.type_code==place_type_code_id).with_entities(Place.type).distinct().all()]

    places = PlaceQuery(filter_selected['search'], 
                        filter_selected['area_gu'], 
                        filter_selected['type'],
                        filter_selected['time_from_now'],
                        filter_selected['page']).get_result()

    places = filtering_time_from_now(places, filter_selected['time_from_now'])
    like_place_ids = [i[0] for i in UserQuery(current_user).get_result()] # 유저가 좋아하는 장소 id들
    for place in places:
        place_time = getattr(place, f"{today_yoil_eng}_opening_hours")
        if place_time in [NULL, '정보없음', '정보 없음']:
            setattr(place, 'status', NULL)
        elif place_time in ['휴무']:
            setattr(place, 'status', "휴무")
        else:
            place_open_time  = int(place_time[:2]) * 100 + int(place_time[3:5])
            place_close_time = int(place_time[-5:-3]) * 100 + int(place_time[-2:])
            time_now_int = time_now[0] * 100 + time_now[1]
            if place_open_time <= time_now_int <= place_close_time:
                setattr(place, 'status', 'open') # '영업 중'
            else:
                setattr(place, 'status', 'close') # '영업 종료'

            if place_close_time < 2400: continue
            setattr(place, f"{today_yoil_eng}_opening_hours", place_time[:5] + f'-{str(int(place_time[-5:-3]) - 24):>02s}:{place_time[-2:]}')
            
            if place_open_time <= time_now_int + 2400 <= place_close_time:
                place['status'] = 'open'  # '영업 중'
    pagemaker = Pagination(places, filter_selected['page'])
    return render_template("pub.html", 
                        current_user=current_user,
                        places=places[pagemaker.start_index: pagemaker.end_index + 1],
                        today_yoil_eng=today_yoil_eng, 
                        today_yoil_kor=today_yoil_kor, 
                        timenow=time_now,
                        NULL=NULL, 
                        KAKAO_JAVASCRIPT_KEY=KAKAO_JAVASCRIPT_KEY, 
                        areas=areas, 
                        types=place_types, 
                        search=filter_selected['search'],
                        area=filter_selected['area_gu'],
                        type=filter_selected['type'],
                        timefromnow=filter_selected['time_from_now'],
                        like_place_ids=like_place_ids,

                        page=filter_selected['page'], 
                        total_page=pagemaker.total_page,
                        pagination_start=pagemaker.pagination_start, 
                        pagination_end=pagemaker.pagination_end,
                        move_page_front=pagemaker.move_page_front, 
                        move_page_back=pagemaker.move_page_back,

                        url='pub.index')

@bp.route('/like_place')
def like_places():
    print(f"[pub.index] username: {current_user.nickname}")

    filter_selected = {
        'search': request.args.get('search', default='', type=str),
        'area_gu': request.args.get('area', default='', type=str),
        'type': request.args.get('type', default='', type=str),
        'time_from_now': request.args.get('timefromnow', default=0, type=int),
        'page': request.args.get('page', default=1, type=int)
    }

    areas = [place[0] for place in Place.query.with_entities(Place.address_gu).distinct().all()]
    place_type_code_id = TypeCode.query.filter(TypeCode.type=="술집").first().id
    place_types = [place[0] for place in Place.query.filter(Place.type_code==place_type_code_id).with_entities(Place.type).distinct().all()]

    places = PlaceQuery(filter_selected['search'], 
                        filter_selected['area_gu'], 
                        filter_selected['type'],
                        filter_selected['time_from_now'],
                        filter_selected['page'],
                        join_user=current_user).get_result()

    places = filtering_time_from_now(places, filter_selected['time_from_now'])
    like_place_ids = [i[0] for i in UserQuery(current_user).get_result()] # 유저가 좋아하는 장소 id들
    for place in places:
        place_time = getattr(place, f"{today_yoil_eng}_opening_hours")
        if place_time in [NULL, '정보없음', '정보 없음']:
            setattr(place, 'status', NULL)
        elif place_time in ['휴무']:
            setattr(place, 'status', "휴무")
        else:
            place_open_time  = int(place_time[:2]) * 100 + int(place_time[3:5])
            place_close_time = int(place_time[-5:-3]) * 100 + int(place_time[-2:])
            time_now_int = time_now[0] * 100 + time_now[1]
            if place_open_time <= time_now_int <= place_close_time:
                setattr(place, 'status', 'open') # '영업 중'
            else:
                setattr(place, 'status', 'close') # '영업 종료'

            if place_close_time < 2400: continue
            setattr(place, f"{today_yoil_eng}_opening_hours", place_time[:5] + f'-{str(int(place_time[-5:-3]) - 24):>02s}:{place_time[-2:]}')
            
            if place_open_time <= time_now_int + 2400 <= place_close_time:
                place['status'] = 'open'  # '영업 중'
    pagemaker = Pagination(places, filter_selected['page'])
    return render_template("pub.html", 
                        current_user=current_user,
                        places=places[pagemaker.start_index: pagemaker.end_index + 1],
                        today_yoil_eng=today_yoil_eng, 
                        today_yoil_kor=today_yoil_kor, 
                        timenow=time_now,
                        NULL=NULL, 
                        KAKAO_JAVASCRIPT_KEY=KAKAO_JAVASCRIPT_KEY, 
                        areas=areas, 
                        types=place_types, 
                        search=filter_selected['search'],
                        area=filter_selected['area_gu'],
                        type=filter_selected['type'],
                        timefromnow=filter_selected['time_from_now'],
                        like_place_ids=like_place_ids,

                        page=filter_selected['page'], 
                        total_page=pagemaker.total_page,
                        pagination_start=pagemaker.pagination_start, 
                        pagination_end=pagemaker.pagination_end,
                        move_page_front=pagemaker.move_page_front, 
                        move_page_back=pagemaker.move_page_back,

                        url='pub.index')

def filtering_time_from_now(places, time_from_now):
    if time_from_now:  # ! 시간 필터 클릭 시 추가
        places = []
        for place in places:
            time = getattr(place, today_yoil_eng + "_opening_hours")
            if time not in [NULL, '휴무', '정보없음', '정보 없음']:
                open = int(time[:2]) * 100 + int(time[3:5])
                close = int(time[-5:-3]) * 100 + int(time[-2:])
                time_now_int = time_now[0] * 100 + time_now[1]
            # ! 지금도 열고, 이따도 여는 곳들만 보여주기
            if (open <= time_now_int <= close 
                or open <= time_now_int + 2400 <= close) \
                    and \
                    (open <= time_now_int + time_from_now * 100 <= close \
                     or open <= time_now_int + time_from_now * 100 + 2400 <= close):
                places.append(place)
        return places
    return places