import csv

def processed_data_to_csv(before_file, after_file):
    processed_data = []
    null = "정보 없음"

    # csv 파일 불러와서 영업시간 데이터 전처리
    with open(before_file, 'r', encoding= 'UTF-8') as file:
        csvReader = csv.DictReader(file)
        for line in csvReader:
            name = line['name']
            type = line['type']
            star_rating = line['star_rating']
            review_sum = line['review_sum']
            address = line['address']
            open_info = line['time_info']
            contact = line['contact']

            if star_rating == null:
                star_rating = 0.0

            open_info_by_day = {'월': {"opening_hours": null, "last_order_time": null},
                                     '화': {"opening_hours": null, "last_order_time": null},
                                     '수': {"opening_hours": null, "last_order_time": null},
                                     '목': {"opening_hours": null, "last_order_time": null},
                                     '금': {"opening_hours": null, "last_order_time": null},
                                     '토': {"opening_hours": null, "last_order_time": null},
                                     '일': {"opening_hours": null, "last_order_time": null} }
            open_info = open_info.replace("'", "").strip('[[').strip(']]').split('], [')
            
            for day in open_info[1:]: # 0번째는 현재 영업중 정보
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
                    open_time = time_info[i-6 : i-1]
                    close_time = time_info[i+2: i+7]
                    open_hour = int(open_time[:2])
                    open_minute = int(open_time[3:])
                    close_hour = int(close_time[:2])
                    close_minute = int(close_time[3:])
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

                # print(yoil, name, len(yoil)) # test debug
                try:
                    if yoil in ["매일"]:
                        # 모든 요일 처리
                        for key in open_info_by_day.keys():
                            open_info_by_day[key] = {"opening_hours": time_info, "last_order_time": day_last_order}
                    elif yoil[0] in ['월', '화', '수', '목', '금', '토', '일']:
                        open_info_by_day[yoil] = {"opening_hours": time_info, "last_order_time": day_last_order}
                except:
                    pass
                                
            keys = ['name', 'type', 'star_rating', 'review_sum', 'address', 
                    '월opening_hours', '월last_order_time',
                    '화opening_hours', '화last_order_time',
                    '수opening_hours', '수last_order_time',
                    '목opening_hours', '목last_order_time',
                    '금opening_hours', '금last_order_time',
                    '토opening_hours', '토last_order_time',
                    '일opening_hours', '일last_order_time',
                    'contact']
            
            values = [name, type, star_rating, review_sum, address, 
                      open_info_by_day['월']['opening_hours'], open_info_by_day['월']['last_order_time'],
                      open_info_by_day['화']['opening_hours'], open_info_by_day['화']['last_order_time'],
                      open_info_by_day['수']['opening_hours'], open_info_by_day['수']['last_order_time'],
                      open_info_by_day['목']['opening_hours'], open_info_by_day['목']['last_order_time'],
                      open_info_by_day['금']['opening_hours'], open_info_by_day['금']['last_order_time'],
                      open_info_by_day['토']['opening_hours'], open_info_by_day['토']['last_order_time'],
                      open_info_by_day['일']['opening_hours'], open_info_by_day['월']['last_order_time'],
                      contact]
            processed_data.append(dict(zip(keys, values)))

    # csv 파일에 저장
    with open(after_file, 'w', encoding= 'UTF-8') as file:
            csvWriter = csv.DictWriter(file, fieldnames=keys)
            csvWriter.writeheader()
            for row in processed_data:
                csvWriter.writerow(row)
                
    print(f'{after_file} 생성이 완료되었습니다.')