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
    filter_selected = {
        'search': request.args.get('search', default='', type=str),
        'area_gu': request.args.get('area', default='', type=str),
        'type': request.args.get('type', default='', type=str),
        'time_from_now': request.args.get('timefromnow', default=0, type=int),
        'page': request.args.get('page', default=1, type=int)
    }

    pub_place_type_code_id = TypeCode.query.filter(TypeCode.type=="술집").first().id
    areas = [place[0] for place in Place.query.with_entities(Place.address_gu).distinct().all()]
    place_types = [place[0] for place in Place.query.filter(Place.type_code==pub_place_type_code_id).with_entities(Place.type).distinct().all()]

    places = PlaceQuery(filter_selected['search'], 
                        filter_selected['area_gu'], 
                        filter_selected['type'],
                        filter_selected['time_from_now'],
                        filter_selected['page']).get_result()

    # places = Place.query.with_entities(Place, func.concat(Place.address_si, ' ', Place.address_gu, ' ', Place.address_lo, ' ', Place.address_detail).label('full_address')).all()
    # print("[디버그]: ")
    # for place in places:
    #     print(place)

    places         = filtering_time_from_now(places, filter_selected['time_from_now'])
    print(places[0])
    places_data    = filtering_place_user_like(places, current_user)
    like_place_ids = [i[0] for i in UserQuery(current_user).get_result()]
    for place in places_data:
        place_time = place[f"{today_yoil_eng}_opening_hours"]

        if place_time in [NULL, '정보없음', '정보 없음']:
            place['status'] = NULL
        elif place_time in ['휴무']:
            place['status'] = '휴무'
        else:
            place_open_time  = int(place_time[:2]) * 100 + int(place_time[3:5])
            place_close_time = int(place_time[-5:-3]) * 100 + int(place_time[-2:])
            time_now_int = time_now[0] * 100 + time_now[1]
            if place_open_time <= time_now_int <= place_close_time:
                place['status'] = 'open'  # '영업 중'
            else:
                place['status'] = 'close'  # '영업 종료'

            if place_close_time >= 2400:
                place[f"{today_yoil_eng}_opening_hours"] = place_time[:5] + f'-{str(int(place_time[-5:-3]) - 24):>02s}:{place_time[-2:]}'
                if place_open_time <= time_now_int + 2400 <= place_close_time:
                    place['status'] = 'open'  # '영업 중'

    pagemaker = Pagination(places_data, filter_selected['page'])

    #? 기본 정렬: 별점 순 
    #? (얘보다 좀 더 빠름 <- place_data = sorted(place_data, key = lambda x: x['star_rating'], reverse=True) )
    places_data = sorted(places_data, key=itemgetter('star_rating'), reverse=True)

    print(f"[pub.index] username: {current_user.nickname}")
    return render_template("pub.html", 
                           today_yoil_eng=today_yoil_eng, 
                           today_yoil_kor=today_yoil_kor, 
                           timenow=time_now,
                           NULL=NULL, 
                           KAKAO_JAVASCRIPT_KEY=KAKAO_JAVASCRIPT_KEY, 
                           current_user=current_user,
                           areas=areas, 
                           types=place_types, 
                           search=filter_selected['search'],
                           area=filter_selected['area_gu'],
                           type=filter_selected['type'],
                           timefromnow=filter_selected['time_from_now'],
                           # likeplace_data=like_place_data,
                           place_data=places_data[pagemaker.start_index: pagemaker.end_index + 1],
                           page=filter_selected['page'], 
                           total_page=pagemaker.total_page,
                           pagination_start=pagemaker.pagination_start, 
                           pagination_end=pagemaker.pagination_end,
                           move_page_front=pagemaker.move_page_front, 
                           move_page_back=pagemaker.move_page_back,
                           like_place_ids=like_place_ids,
                           url='pub.index')

@bp.route('/like_place')
def like_places():
    search = request.args.get('search', default='', type=str)
    area = request.args.get('area', default='', type=str)
    type = request.args.get('type', default='', type=str)
    time_from_now = request.args.get('timefromnow', default=0, type=int)
    page = request.args.get('page', default=1, type=int)

    pub_place_type_id = TypeCode.query.filter_by(type="술집").first()
    areas = [i[0] for i in Place.query.with_entities(Place.address_gu).distinct().all()]
    types = [i[0] for i in
             Place.query.filter_by(type_code=pub_place_type_id).with_entities(Place.type).distinct().all()]

    if area:  # 지역 필터 사용 시
        like_places_before = Place.query.join(UserLike).join(User).filter(Place.address_gu == area,
                                                                          Place.type_code == pub_place_type_id,
                                                                          Place.id == UserLike.placeid,
                                                                          UserLike.userid == User.id).all()
    else:  # 지역 필터가 전체일 시
        like_places_before = Place.query.join(UserLike).join(User).filter(Place.type_code == pub_place_type_id,
                                                                          Place.id == UserLike.placeid,
                                                                          UserLike.userid == User.id).all()
    like_places = []

    for place in like_places_before:
        print(place)
        like_places.append({
            'id': place.id,
            'uuid': place.uuid,
            'type_code': place.type_code,
            'name': place.name,
            'type': place.type,
            'star_rating': place.star_rating,
            'address_si': place.address_si,
            'address_gu': place.address_gu,
            'address_lo': place.address_lo,
            'address_detail': place.address_detail,
            'address': f'{place.address_si} {place.address_gu} {place.address_lo} {place.address_detail}',
            'contact': place.contact,
            'lat': place.lat,
            'lng': place.lng,
            'naver_place_id': place.naver_place_id,
            'place_url': place.place_url,
            'naver_road_url': place.naver_road_url,
            'kakao_road_url': place.kakao_road_url,
            'review_total': place.review_total,
            'mon_opening_hours': place.mon_opening_hours,
            'mon_last_order_time': place.mon_last_order_time,
            'tue_opening_hours': place.tue_opening_hours,
            'tue_last_order_time': place.tue_last_order_time,
            'wed_opening_hours': place.wed_opening_hours,
            'wed_last_order_time': place.wed_last_order_time,
            'thu_opening_hours': place.thu_opening_hours,
            'thu_last_order_time': place.thu_last_order_time,
            'fri_opening_hours': place.fri_opening_hours,
            'fri_last_order_time': place.fri_last_order_time,
            'sat_opening_hours': place.sat_opening_hours,
            'sat_last_order_time': place.sat_last_order_time,
            'sun_opening_hours': place.sun_opening_hours,
            'sun_last_order_time': place.sun_last_order_time,
            'created_at': place.created_at,
        })

    page_maker = Pagination(like_places, page)
    return render_template('like_pub.html', today_yoil_eng=today_yoil_eng, today_yoil_kor=today_yoil_kor,
                           areas=areas, types=types, search=search, area=area, type=type, timefromnow=time_from_now,
                           NULL=NULL, KAKAO_JAVASCRIPT_KEY=KAKAO_JAVASCRIPT_KEY, current_user=current_user,
                           like_places=like_places[page_maker.start_index: page_maker.end_index + 1],
                           page=page, total_page=page_maker.total_page, pagination_start=page_maker.pagination_start,
                           pagination_end=page_maker.pagination_end, move_page_front=page_maker.move_page_front,
                           move_page_back=page_maker.move_page_back,
                           url='pub.like_places')

def filtering_time_from_now(places, time_from_now):
    if time_from_now:  # ! 시간 필터 클릭 시 추가
        places = []
        for place in places:
            place_time = place[today_yoil_eng + "_opening_hours"]
            if place_time not in [NULL, '휴무', '정보없음', '정보 없음']:
                place_open_time = int(place_time[:2]) * 100 + int(place_time[3:5])
                place_close_time = int(place_time[-5:-3]) * 100 + int(place_time[-2:])
                time_now_int = time_now[0] * 100 + time_now[1]
            # ! 지금도 열고, 이따도 여는 곳들만 보여주기
            if (place_open_time <= time_now_int <= place_close_time 
                or place_open_time <= time_now_int + 2400 <= place_close_time) \
                    and \
                    (place_open_time <= time_now_int + time_from_now * 100 <= place_close_time \
                     or place_open_time <= time_now_int + time_from_now * 100 + 2400 <= place_close_time):
                places.append(place)
        return places
    return places


def filtering_place_user_like(places, current_user):
    # places_data = []
    for place in places:
        if current_user.is_authenticated:  # ! 로그인한 유저가 있으면
            is_like = User.query.join(UserLike).filter(UserLike.placeid == place.id,
                                                       UserLike.userid == current_user.id).first()
        else:
            is_like = None

        # places_data.append({
        #     'is_like': is_like,
        #     'id': place.id,
        #     'uuid': place.uuid,
        #     'type_code': place.type_code,
        #     'name': place.name,
        #     'type': place.type,
        #     'star_rating': place.star_rating,
        #     'address_si': place.address_si,
        #     'address_gu': place.address_gu,
        #     'address_lo': place.address_lo,
        #     'address_detail': place.address_detail,
        #     'address': f'{place.address_si} {place.address_gu} {place.address_lo} {place.address_detail}',
        #     'contact': place.contact,
        #     'lat': place.lat,
        #     'lng': place.lng,
        #     'naver_place_id': place.naver_place_id,
        #     'place_url': place.place_url,
        #     'naver_road_url': place.naver_road_url,
        #     'kakao_road_url': place.kakao_road_url,
        #     'review_total': place.review_total,
        #     'mon_opening_hours': place.mon_opening_hours,
        #     'mon_last_order_time': place.mon_last_order_time,
        #     'tue_opening_hours': place.tue_opening_hours,
        #     'tue_last_order_time': place.tue_last_order_time,
        #     'wed_opening_hours': place.wed_opening_hours,
        #     'wed_last_order_time': place.wed_last_order_time,
        #     'thu_opening_hours': place.thu_opening_hours,
        #     'thu_last_order_time': place.thu_last_order_time,
        #     'fri_opening_hours': place.fri_opening_hours,
        #     'fri_last_order_time': place.fri_last_order_time,
        #     'sat_opening_hours': place.sat_opening_hours,
        #     'sat_last_order_time': place.sat_last_order_time,
        #     'sun_opening_hours': place.sun_opening_hours,
        #     'sun_last_order_time': place.sun_last_order_time,
        #     'created_at': place.created_at,
        # })
    # return places_data