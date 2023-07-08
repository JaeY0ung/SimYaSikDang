from naver_crawler.crawler_ver_2 import naver_crawler
from csv_to_excel import csv_to_excel
import areas_info
from data_processing import processed_data_to_csv

# areas_dict = areas_info.areas_dict_ver2
areas_dict = areas_info.areas_dict_test


# # 지역별 크롤링 시작
# for gu, dong in areas_dict.items():
#     for area in dong:
#         naver_crawler(area) # 크롤링
#         csv_to_excel(area)  # 엑셀에 데이터 저장
#         processed_data_to_csv(area) # 데이터 처리하여 csv 파일에 저장

naver_crawler("일산") # 크롤링
csv_to_excel("일산")  # 엑셀에 데이터 저장
processed_data_to_csv("일산") # 데이터 처리하여 csv 파일에 저장