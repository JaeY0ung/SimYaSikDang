from Crawler.crawler import naver_crawler
from FileTransform.fileTransform import csv_to_excel
from DataProcessing.dataProcesing import processed_data_to_csv
import src.seoul_area_data as seoul_area_data

areas_dict = seoul_area_data.areas_dict_test

# # 데이터 크롤링하여 csv파일과 엑셀파일로 저장
# for gu, dong in areas_dict.items():
#     for area in dong:
#         naver_crawler(area)
#         csv_to_excel(f"./csv/{area}.csv", f"./excel/{area}.xlsx")  # 엑셀에 데이터 저장

# 영업시간 데이터 처리하여 csv 파일과 엑셀파일로 저장
for gu, dong in areas_dict.items():
    for area in dong:          
        processed_data_to_csv(area)
        csv_to_excel(f"./csv/{area}_processed.csv", f"./excel/{area}_processed.xlsx")