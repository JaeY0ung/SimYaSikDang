import csv

def processed_data_to_csv(area):
    processed_data = []
    null = "정보 없음"

    # csv 파일 불러와서 영업시간 데이터 전처리
    with open(f'./csv/{area}술집.csv', 'r', encoding= 'UTF-8') as file:
        csvReader = csv.reader(file)
        processed_data.append(dict(zip(["월","화","수","목","금","토","일"], ["월","화","수","목","금","토","일"])))
        next(csvReader) # 헤더 뺴고 읽기
        for line in csvReader:
            shop_open_info_by_day = {'월': null,
                                    '화': null,
                                    '수': null,
                                    '목': null,
                                    '금': null,
                                    '토': null,
                                    '일': null}
            shop_open_info = line[4]
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
                
            processed_data.append(shop_open_info_by_day.values())

    # csv 파일에 저장
    with open(f'./csv/{area}술집_processed_opentime_data.csv', 'w', encoding= 'UTF-8') as file:
            csvWriter = csv.writer(file)
            csvWriter.writerow(processed_data[0])
            for row in processed_data[1:]:
                csvWriter.writerow(row)
    print(f'./csv/{area}술집_processed_opentime_data.csv 생성이 완료되었습니다.')