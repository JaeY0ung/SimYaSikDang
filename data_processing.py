import csv

def processed_data_to_csv(area):
    processed_data = []
    null = "정보 없음"

    # csv 파일 불러와서 영업시간 데이터 전처리
    with open(f'./csv/{area}술집.csv', 'r', encoding= 'UTF-8') as file:
        csvReader = csv.DictReader(file)
        for line in csvReader:
            shop_name = line['shop_name']
            shop_type = line['shop_type']
            shop_star_rating = line['shop_star_rating']
            shop_address = line['shop_address']
            shop_open_info = line['shop_time_info']
            shop_contact = line['shop_contact']

            shop_open_info_by_day = {'월': null,
                                     '화': null,
                                     '수': null,
                                     '목': null,
                                     '금': null,
                                     '토': null,
                                     '일': null }
            shop_open_info = shop_open_info.replace("'", "").strip('[[').strip(']]').split('], [')
            
            for day in shop_open_info[1:]:
                day = day.split(', ')

                if len(day) > 1:
                    day_of_the_week, day_info = day[0], day[1]
                else:
                    day_of_the_week, day_info = day[0], null
                    
                if '매일' in day_of_the_week:
                    if shop_open_info_by_day['월'] == null:
                        shop_open_info_by_day['월'] = day_info
                    if shop_open_info_by_day['화'] == null:
                        shop_open_info_by_day['화'] = day_info
                    if shop_open_info_by_day['수'] == null:
                        shop_open_info_by_day['수'] = day_info
                    if shop_open_info_by_day['목'] == null:
                        shop_open_info_by_day['목'] = day_info
                    if shop_open_info_by_day['금'] == null:
                        shop_open_info_by_day['금'] = day_info
                    if shop_open_info_by_day['토'] == null:
                        shop_open_info_by_day['토'] = day_info
                    if shop_open_info_by_day['일'] == null:
                        shop_open_info_by_day['일'] = day_info

                elif '월' in day_of_the_week:
                    shop_open_info_by_day['월'] = day_info
                elif '화' in day_of_the_week:
                    shop_open_info_by_day['화'] = day_info
                elif '수' in day_of_the_week:
                    shop_open_info_by_day['수'] = day_info
                elif '목' in day_of_the_week:
                    shop_open_info_by_day['목'] = day_info
                elif '금' in day_of_the_week:
                    shop_open_info_by_day['금'] = day_info
                elif '토' in day_of_the_week:
                    shop_open_info_by_day['토'] = day_info
                elif '일' in day_of_the_week:
                    shop_open_info_by_day['일'] = day_info
                
                
            keys = ['shop_name', 'shop_type', 'shop_star_rating', 'shop_address', 'shop_open_info', 'shop_contact']
            values = [shop_name, shop_type, shop_star_rating, shop_address, list(shop_open_info_by_day.items()), shop_contact]
            processed_data.append(dict(zip(keys, values)))

    # csv 파일에 저장
    with open(f'./csv/{area}술집_processed_opentime_data.csv', 'w', encoding= 'UTF-8') as file:
            csvWriter = csv.DictWriter(file, fieldnames=keys)
            csvWriter.writeheader()
            for row in processed_data:
                csvWriter.writerow(row)
    print(f'./csv/{area}술집_processed_opentime_data.csv 생성이 완료되었습니다.')