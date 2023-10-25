from crawler.crawler import NaverCrawler
from crawler.fileTransform import csv_to_xlsx
from crawler.dataProcesing import processed_data_to_csv
from constant import dict_area_gu_to_dong, dict_area_kor_to_eng, dict_searchtype_to_code
from datetime import datetime
import time

#? 데이터 크롤링하여 csv파일과 엑셀파일로 저장
class Data_Crawl_and_Process:
    def __init__(self):
        print(f'크롤링 날짜: {datetime.today().strftime("%Y-%m-%d")}')
    
    def get_one(self, area_kor, type_kor):
        area_eng  = dict_area_kor_to_eng[area_kor]
        type_code = dict_searchtype_to_code[type_kor]
        try:
            self.crawler = NaverCrawler()
            self.crawler.naver_crawler(area_kor, type_kor)
            csv_to_xlsx(f"./crawler/csv/{area_eng}_{type_code}.csv", f"./crawler/xlsx/{area_eng}_{type_code}.xlsx") 
        except:
            print(f'{area_kor} {type_kor} 크롤링/데이터저장 실패')
        try:
            processed_data_to_csv(area_kor, type_code,
                                f"./crawler/csv/{area_eng}_{type_code}.csv", 
                                f"./crawler/csv/{area_eng}_{type_code}_processed.csv")
            print('(중간) processed_data_to_csv 완료')
            csv_to_xlsx(f"./crawler/csv/{area_eng}_{type_code}_processed.csv", f"./crawler/xlsx/{area_eng}_{type_code}_processed.xlsx")
            print(f'{area_kor} {type_kor} 데이터 가공하여 저장 성공')
        except:
            print(f'{area_kor} {type_kor} 데이터 가공,저장 실패')
        
    def get_one_area(self, area_kor):
        for type_kor in dict_searchtype_to_code.keys():
            self.get_one(area_kor, type_kor)

    def get_all_area(self):
        for dongs in dict_area_gu_to_dong.values():
            for dong in dongs:
                self.get_one_area(dong)
    
    def get_pub_only(self):
        for dongs in dict_area_gu_to_dong.values():
            for dong in dongs:
                self.get_one(dong, '술집')

    def get_cafe_only(self):
        for dongs in dict_area_gu_to_dong.values():
            for dong in dongs:
                self.get_one(dong, '카페')

    def get_restaurant_only(self):
        for dongs in dict_area_gu_to_dong.values():
            for dong in dongs:
                self.get_one(dong, '식당')