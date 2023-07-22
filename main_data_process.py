from Crawler.crawler import naver_crawler
from FileTransform.fileTransform import csv_to_excel
from DataProcessing.dataProcesing import processed_data_to_csv
from src.area import areas_dict_ver1, areas_dict_ver2, areas_dict_test, k_to_e

# 데이터 크롤링하여 csv파일과 엑셀파일로 저장
for gu, dong in areas_dict_test.items():
    for area in dong:
        try:
            naver_crawler(area)
            csv_to_excel(f"./csv/{k_to_e[area]}.csv", f"./excel/{k_to_e[area]}.xlsx")  # 엑셀에 데이터 저장
            print(f'{area} 크롤링 성공')
        except:
            print(f'{area} 크롤링 실패')
     
        try:
            processed_data_to_csv(f'./csv/{k_to_e[area]}.csv', f'./csv/{k_to_e[area]}_processed.csv')
            csv_to_excel(f"./csv/{k_to_e[area]}_processed.csv", f"./excel/{k_to_e[area]}_processed.xlsx")
            print(f'{area} 데이터처리 성공')
        except:
            print(f'{area} 데이터처리 실패')

# # 영업시간 데이터 처리하여 csv 파일과 엑셀파일로 저장
# for gu, dong in areas_dict_test.items():
#     for area in dong:          
#         processed_data_to_csv(f'./csv/{k_to_e[area]}.csv', f'./csv/{k_to_e[area]}_processed.csv')
#         csv_to_excel(f"./csv/{k_to_e[area]}_processed.csv", f"./excel/{k_to_e[area]}_processed.xlsx")