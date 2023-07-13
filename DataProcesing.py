import csv

def processed_data_to_csv(area):
    processed_data = []
    null = "정보 없음"

    # csv 파일 불러와서 영업시간 데이터 전처리
    with open(f'./csv/{area}.csv', 'r', encoding= 'UTF-8') as file:
        csvReader = csv.DictReader(file)
        for line in csvReader:
            shop_name = line['shop_name']
            shop_type = line['shop_type']
            shop_star_rating = line['shop_star_rating']
            shop_address = line['shop_address']
            shop_open_info = line['shop_time_info']
            shop_contact = line['shop_contact']

            shop_open_info_by_day = {'월': {"opening_hours": null, "last_order_time": null},
                                     '화': {"opening_hours": null, "last_order_time": null},
                                     '수': {"opening_hours": null, "last_order_time": null},
                                     '목': {"opening_hours": null, "last_order_time": null},
                                     '금': {"opening_hours": null, "last_order_time": null},
                                     '토': {"opening_hours": null, "last_order_time": null},
                                     '일': {"opening_hours": null, "last_order_time": null} }
            shop_open_info = shop_open_info.replace("'", "").strip('[[').strip(']]').split('], [')
            
            for day in shop_open_info[1:]: # 0번째는 현재 영업중 정보
                day = day.split(', ')
                if len(day) >= 3:
                    yoil, time_info, day_last_order = day[0], day[1], day[2]
                elif len(day) >= 2:
                    yoil, time_info, day_last_order = day[0], day[1], null
                elif len(day) == 1:
                    yoil, time_info, day_last_order = day[0], null, null
                else:
                    yoil, time_info, day_last_order = null, null, null
                    
                if '휴무' in time_info:
                    time_info = "휴무"

                elif '-' in time_info and '/' not in time_info:
                    i =  time_info.index('-')
                    start = time_info[i-6 : i-1]
                    end = time_info[i+2: i+7]
                    # print(shop_name, start, end) # debug test
                    start_hour = int(start[:2])
                    start_minute = int(start[3:])
                    end_hour = int(end[:2])
                    end_minute = int(end[3:])
                    if start_hour > end_hour:
                        end_hour += 24
                    time_info = f"{start_hour:02d}:{start_minute:02d}-{end_hour:02d}:{end_minute:02d}"

                if '라스트오더' in day_last_order:
                    if '시' in day_last_order:
                        if '분' in day_last_order: # 21시 30분에 라스트오더
                            day_last_order = f"{int(day_last_order.split('시', '분')[0]):02d}:{int(day_last_order.split('시', '분')[1]):02d}"
                        else: #21시에 라스트 오더 (이건 있는 경우인지 모르겠음)
                            day_last_order = f"{int(day_last_order.split('시')[0]):02d}:00"
                    else: # ex. 23:00 라스트오더
                        day_last_order = day_last_order.split(' ')[0]

                # print(yoil, shop_name, len(yoil)) # test debug
                try:
                    if yoil in ["매일"]:
                        # 모든 요일 처리
                        for key in shop_open_info_by_day.keys():
                            shop_open_info_by_day[key] = {"opening_hours": time_info, "last_order_time": day_last_order}
                    elif yoil[0] in ['월', '화', '수', '목', '금', '토', '일']:
                        shop_open_info_by_day[yoil] = {"opening_hours": time_info, "last_order_time": day_last_order}
                except:
                    pass
                                
            keys = ['shop_name', 'shop_type', 'shop_star_rating', 'shop_address', 
                    '월opening_hours', '월last_order_time',
                    '화opening_hours', '화last_order_time',
                    '수opening_hours', '수last_order_time',
                    '목opening_hours', '목last_order_time',
                    '금opening_hours', '금last_order_time',
                    '토opening_hours', '토last_order_time',
                    '일opening_hours', '일last_order_time',
                    'shop_contact']
            
            values = [shop_name, shop_type, shop_star_rating, shop_address, 
                      shop_open_info_by_day['월']['opening_hours'], shop_open_info_by_day['월']['last_order_time'],
                      shop_open_info_by_day['화']['opening_hours'], shop_open_info_by_day['화']['last_order_time'],
                      shop_open_info_by_day['수']['opening_hours'], shop_open_info_by_day['수']['last_order_time'],
                      shop_open_info_by_day['목']['opening_hours'], shop_open_info_by_day['목']['last_order_time'],
                      shop_open_info_by_day['금']['opening_hours'], shop_open_info_by_day['금']['last_order_time'],
                      shop_open_info_by_day['토']['opening_hours'], shop_open_info_by_day['토']['last_order_time'],
                      shop_open_info_by_day['일']['opening_hours'], shop_open_info_by_day['월']['last_order_time'],
                      shop_contact]
            processed_data.append(dict(zip(keys, values)))

    # csv 파일에 저장
    with open(f'./csv/{area}_processed.csv', 'w', encoding= 'UTF-8') as file:
            csvWriter = csv.DictWriter(file, fieldnames=keys)
            csvWriter.writeheader()
            for row in processed_data:
                csvWriter.writerow(row)
                
    print(f'./csv/{area}_processed.csv 생성이 완료되었습니다.')