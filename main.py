from Naver_Crawler.crawler_ver_2 import naver_crawler
from csv_to_excel import csv_to_excel
import areas_info

areas_dict = areas_info.areas_dict

# 지역별 크롤링 시작
for gu, dong in areas_dict.items():
    for area in dong:
        naver_crawler(area) # 크롤링
        csv_to_excel(area)  # 엑셀에 데이터 저장