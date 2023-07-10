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

            shop_open_info_by_day = {'월': {"open_time": null, "last_order_time": null},
                                     '화': {"open_time": null, "last_order_time": null},
                                     '수': {"open_time": null, "last_order_time": null},
                                     '목': {"open_time": null, "last_order_time": null},
                                     '금': {"open_time": null, "last_order_time": null},
                                     '토': {"open_time": null, "last_order_time": null},
                                     '일': {"open_time": null, "last_order_time": null} }
            shop_open_info = shop_open_info.replace("'", "").strip('[[').strip(']]').split('], [')
            
            for day in shop_open_info[1:]: # 0번째는 현재 영업중 정보
                day = day.split(', ')
                if len(day) >= 3:
                    day_of_the_week, day_info, day_last_order = day[0], day[1], day[2]
                elif len(day) >= 2:
                    day_of_the_week, day_info, day_last_order = day[0], day[1], null
                else:
                    day_of_the_week, day_info, day_last_order = day[0], null, null
                    
                if '휴무' in day_info:
                    day_info = "휴무"

                if '라스트오더' in day_last_order:
                    if '시' in day_last_order:
                        if '분' in day_last_order: # 21시 30분에 라스트오더
                            day_last_order = day_last_order.split('시', '분')[0] + ':' +day_last_order.split('시', '분')[1]
                        else: #21시에 라스트오더 (이건 있는 경우인지 모르겠음)
                            day_last_order = day_last_order.split('시')[0] + ':00'
                    else: # 23:00 라스트오더
                        day_last_order = day_last_order.split(' ')[0]
                        
                if day_of_the_week in ['월', '화', '수', '목', '금', '토', '일']:
                    shop_open_info_by_day[day_of_the_week] = {"open_time": day_info, "last_order_time": day_last_order}
                                
            keys = ['shop_name', 'shop_type', 'shop_star_rating', 'shop_address', 'shop_open_info', 'shop_contact']
            values = [shop_name, shop_type, shop_star_rating, shop_address, list(shop_open_info_by_day.items()), shop_contact]
            processed_data.append(dict(zip(keys, values)))

    # csv 파일에 저장
    with open(f'./csv/{area}_processed.csv', 'w', encoding= 'UTF-8') as file:
            csvWriter = csv.DictWriter(file, fieldnames=keys)
            csvWriter.writeheader()
            for row in processed_data:
                csvWriter.writerow(row)
    print(f'./csv/{area}_processed.csv 생성이 완료되었습니다.')