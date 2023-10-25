import pandas as pd
import csv
from constant import dict_area_kor_to_eng
from models import Place, TypeCode, db
import uuid

def csv_to_xlsx(csvfile, xlsxfile):
    csvReader = pd.read_csv(csvfile)
    save_xlsx = pd.ExcelWriter(xlsxfile)
    csvReader.to_excel(save_xlsx, index = False)
    save_xlsx.save()

def load_csv(csvfile):
    data = []
    with open(csvfile, newline="") as file:
        csvReader = csv.DictReader(file)
        for place in csvReader:
            data.append(place)
    return data

def naver_place_csv_to_db(dong, code):
    # #! (일회용) place 테이블 데이터 모두 지우기
    # Place.query.delete()
    # db.session.commit()

    # #! (일회용) place 이름이 새로오픈인 거 지우기
    # Place.query.filter_by(name='새로오픈').delete()
    # db.session.commit()

    csvfile = f"./crawler/csv/{dict_area_kor_to_eng[dong]}_{code}_processed.csv"
    
    with open(csvfile, newline="") as file:
        csvReader = csv.DictReader(file)
        for place in csvReader:
            typecode_obj = TypeCode.query.filter_by(code = place['type_code']).first()

            search_place = Place.query.filter_by(
                name           = place['name'],
                type_code      = int(typecode_obj.id),
                naver_place_id = place['naver_place_id'],
            ).first()
            if search_place: # db에 장소가 있으면
                # 향후 type, place_url, naver_road_url, kakao_road_url은 바꾸지 않는다.
                search_place.rating              = place['star_rating']
                search_place.review_total        = place['review_total']
                search_place.address_si          = place['address_si']
                search_place.address_gu          = place['address_gu']
                search_place.address_lo          = place['address_lo']
                search_place.address_detail      = place['address_detail']
                search_place.contact             = place['contact']
                search_place.lat                 = place['lat']
                search_place.lng                 = place['lng']
                search_place.naver_place_id      = place['naver_place_id']
                search_place.place_url           = place['place_url']
                search_place.naver_road_url      = place['naver_road_url']
                search_place.kakao_road_url      = place['kakao_road_url']
                search_place.mon_opening_hours   = place['mon_opening_hours']
                search_place.mon_last_order_time = place['mon_last_order_time']
                search_place.tue_opening_hours   = place['tue_opening_hours']
                search_place.tue_last_order_time = place['tue_last_order_time']
                search_place.wed_opening_hours   = place['wed_opening_hours']
                search_place.wed_last_order_time = place['wed_last_order_time']
                search_place.thu_opening_hours   = place['thu_opening_hours']
                search_place.thu_last_order_time = place['thu_last_order_time']
                search_place.fri_opening_hours   = place['fri_opening_hours']
                search_place.fri_last_order_time = place['fri_last_order_time']
                search_place.sat_opening_hours   = place['sat_opening_hours']
                search_place.sat_last_order_time = place['sat_last_order_time']
                search_place.sun_opening_hours   = place['sun_opening_hours']
                search_place.sun_last_order_time = place['sun_last_order_time']
                search_place.created_at          = place['created_at']
                print(f'존재하는  장소입니다: {search_place.name} update 완료')

            else: #! db에 장소가 없으면
                created_place = Place(
                    uuid                = str(uuid.uuid4()),
                    type_code           = int(typecode_obj.id),
                    name                = place['name'],
                    type                = place['type'],
                    star_rating         = place['star_rating'],
                    review_total        = place['review_total'], #! review_total로 맞추기 (crawler, process, 이 컬럼 변경)
                    address_si          = place['address_si'],
                    address_gu          = place['address_gu'],
                    address_lo          = place['address_lo'],
                    address_detail      = place['address_detail'],
                    contact             = place['contact'],
                    lat                 = place['lat'],
                    lng                 = place['lng'],
                    naver_place_id      = place['naver_place_id'],
                    place_url           = place['place_url'],
                    naver_road_url      = place['naver_road_url'],
                    kakao_road_url      = place['kakao_road_url'],
                    mon_opening_hours   = place['mon_opening_hours'],
                    mon_last_order_time = place['mon_last_order_time'],
                    tue_opening_hours   = place['tue_opening_hours'],
                    tue_last_order_time = place['tue_last_order_time'],
                    wed_opening_hours   = place['wed_opening_hours'],
                    wed_last_order_time = place['wed_last_order_time'],
                    thu_opening_hours   = place['thu_opening_hours'],
                    thu_last_order_time = place['thu_last_order_time'],
                    fri_opening_hours   = place['fri_opening_hours'],
                    fri_last_order_time = place['fri_last_order_time'],
                    sat_opening_hours   = place['sat_opening_hours'],
                    sat_last_order_time = place['sat_last_order_time'],
                    sun_opening_hours   = place['sun_opening_hours'],
                    sun_last_order_time = place['sun_last_order_time'],
                    created_at          = place['created_at'],
                )
                db.session.add(created_place)
                print(f"{created_place.name} 추가 완료")

            db.session.commit()