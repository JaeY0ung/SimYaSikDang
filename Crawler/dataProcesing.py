import csv
from crawler.constant import dict_area_kor_to_eng, NULL
from crawler.naver_api import naver_map_LatLng

def processed_data_to_csv(area_kor, type_code, before_file, after_file):
    processed_data = []
    area_English = dict_area_kor_to_eng[area_kor]
    # csv 파일 불러와서 영업시간 데이터 전처리
    with open(before_file, 'r', encoding= 'UTF-8') as file:
        csvReader = csv.DictReader(file)
        for line in csvReader:
            name          = line['name']
            type          = line['type']
            star_rating   = line['star_rating']
            review_total  = line['review_total']
            address       = line['address']
            opening_hours = line['opening_hours']
            contact       = line['contact']
            place_url     = line["place_url"]
            created_at    = line["created_at"]
            latlng        = naver_map_LatLng(address) # TODO : 현재는 데이터 저장할 때마다 naver_api 호출함 -> 데이터가 update 할 때만 저장하기(filetransform에서 처리)
            lat           = latlng[0]
            lng           = latlng[1]

            #! 별점  
            if star_rating == NULL:
                star_rating = 0.0

            #! 주소
            if address == NULL:
                address_si, address_gu, address_lo, address_detail = NULL, NULL, NULL, NULL
            else:
                address.replace('로',  '로 ')
                address.replace('로  ', '로')
                address_list = address.split()
                address_si     = address_list[0]
                address_gu     = address_list[1]
                address_lo     = address_list[2]
                address_detail = ' '.join(address_list[3:])

            if place_url == NULL:
                naver_place_id, road_url = NULL, NULL
            else:
                naver_place_id = place_url.replace('https://pcmap.place.naver.com/', '').split('/')[1]
                road_url = f"https://map.naver.com/p/directions/-/,,,{ naver_place_id },PLACE_POI/-/walk?c=13.00,0,0,0,dh"

            opening_hours_by_day = {
                                    '월': {"opening_hours": NULL, "last_order_time": NULL},
                                    '화': {"opening_hours": NULL, "last_order_time": NULL},
                                    '수': {"opening_hours": NULL, "last_order_time": NULL},
                                    '목': {"opening_hours": NULL, "last_order_time": NULL},
                                    '금': {"opening_hours": NULL, "last_order_time": NULL},
                                    '토': {"opening_hours": NULL, "last_order_time": NULL},
                                    '일': {"opening_hours": NULL, "last_order_time": NULL} 
                                    }
            opening_hours = opening_hours.replace("'", "").strip('[[').strip(']]').split('], [')
            
            for day in opening_hours[1:]: # 0번째는 현재 영업중 정보
                day = day.split(', ')
                if len(day) >= 3:
                    yoil, time_info, day_last_order = day[0], day[1], day[2]
                elif len(day) >= 2:
                    yoil, time_info, day_last_order = day[0], day[1], NULL
                elif len(day) == 1:
                    yoil, time_info, day_last_order = day[0], NULL, NULL
                else:
                    yoil, time_info, day_last_order = NULL, NULL, NULL
                
                print(f'<{name}> 요일: {yoil}, time_info: {time_info}, 라스트오더: {day_last_order}')
                    
                if '휴무' in time_info:
                    time_info = "휴무"
                elif '-' in time_info and '/' not in time_info:
                    print('time_info:', time_info)
                    i = time_info.index('-')
                    # time_info.replace(' ', '')
                    open_time  = time_info[i-6 : i-1]
                    close_time = time_info[i+2: i+7]
                    if open_time != "":
                        open_hour, open_minute = int(open_time[:2]), int(open_time[3:])
                    else:
                        open_hour, open_minute = 0, 0
                    print(open_hour, open_minute)

                    if close_time != "":
                        close_hour, close_minute = int(close_time[:2]), int(close_time[3:])
                    else:
                        close_hour, close_minute = 23, 59
                    if open_hour > close_hour:
                        close_hour += 24
                    time_info = f"{open_hour:02d}:{open_minute:02d}-{close_hour:02d}:{close_minute:02d}"

                if '라스트오더' in day_last_order:
                    if '시' in day_last_order:
                        if '분' in day_last_order: # 21시 30분에 라스트오더
                            day_last_order = f"{int(day_last_order.split('시', '분')[0]):02d}:{int(day_last_order.split('시', '분')[1]):02d}"
                        else: #21시에 라스트 오더 (이건 있는 경우인지 모르겠음)
                            day_last_order = f"{int(day_last_order.split('시')[0]):02d}:00"
                    else: # ex. 23:00 라스트오더
                        day_last_order = day_last_order.split(' ')[0]

                
                try:
                    if yoil in ["매일"]:
                        # 모든 요일 처리
                        for key in opening_hours_by_day.keys():
                            opening_hours_by_day[key] = {"opening_hours": time_info, "last_order_time": day_last_order}
                    elif yoil[0] in ['월', '화', '수', '목', '금', '토', '일']:
                        opening_hours_by_day[yoil] = {"opening_hours": time_info, "last_order_time": day_last_order}
                except:
                    pass
                                
            keys = ['created_at', 'name', 'type', 'star_rating', 'review_total', 'contact', 'type_code',
                    'address', "address_si", "address_gu", "address_lo",  "address_detail",
                    'lat', 'lng', 'naver_place_id', 'place_url', 'road_url',
                    'mon_opening_hours', 'mon_last_order_time',
                    'tue_opening_hours', 'tue_last_order_time',
                    'wed_opening_hours', 'wed_last_order_time',
                    'thu_opening_hours', 'thu_last_order_time',
                    'fri_opening_hours', 'fri_last_order_time',
                    'sat_opening_hours', 'sat_last_order_time',
                    'sun_opening_hours', 'sun_last_order_time',
                    ]
            
            values = [created_at, name, type, star_rating, review_total, contact, type_code,
                      address, address_si, address_gu, address_lo, address_detail,
                      lat, lng, naver_place_id, place_url, road_url,
                      opening_hours_by_day['월']['opening_hours'], opening_hours_by_day['월']['last_order_time'],
                      opening_hours_by_day['화']['opening_hours'], opening_hours_by_day['화']['last_order_time'],
                      opening_hours_by_day['수']['opening_hours'], opening_hours_by_day['수']['last_order_time'],
                      opening_hours_by_day['목']['opening_hours'], opening_hours_by_day['목']['last_order_time'],
                      opening_hours_by_day['금']['opening_hours'], opening_hours_by_day['금']['last_order_time'],
                      opening_hours_by_day['토']['opening_hours'], opening_hours_by_day['토']['last_order_time'],
                      opening_hours_by_day['일']['opening_hours'], opening_hours_by_day['월']['last_order_time'],
                      ]
            processed_data.append(dict(zip(keys, values)))

    #? csv 파일에 저장
    with open(after_file, 'w', encoding= 'UTF-8') as file:
            csvWriter = csv.DictWriter(file, fieldnames=keys)
            csvWriter.writeheader()
            for row in processed_data:
                csvWriter.writerow(row)
                
    print(f'{after_file} 생성이 완료되었습니다.')