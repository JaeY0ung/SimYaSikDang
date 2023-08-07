from Crawler.crawler import naver_crawler
from FileTransform.fileTransform import csv_to_excel
from DataProcessing.dataProcesing import processed_data_to_csv
from constant import area_k_to_e, set_csvfile_name, set_xlsxfile_name, store_type_k_to_e
from datetime import datetime

#? 데이터 크롤링하여 csv파일과 엑셀파일로 저장
class Data_Crawl_and_Process:
    def __init__(self):
        self.today = datetime.today()
        print(f'크롤링 날짜: {self.today.strftime("%Y-%m-%d")}')
    
    def all(self):
        for area_kor, area_eng in area_k_to_e.items():
            for store_type_kor in store_type_k_to_e.keys():
                try:
                    naver_crawler(area_kor, store_type_kor)
                    #? 엑셀에 크롤링한 데이터 저장
                    csv_to_excel(set_csvfile_name(area_kor, store_type_kor, 'before'), 
                                 set_xlsxfile_name(area_kor, store_type_kor, 'before')) 
                    print(f'{area_kor} 크롤링 성공')
                except:
                    print(f'{area_kor} 크롤링 실패')
                try:
                    processed_data_to_csv(area_kor, 
                                          set_csvfile_name(area_kor, store_type_kor, 'before'),
                                          set_csvfile_name(area_kor, store_type_kor, 'after'))
                    csv_to_excel(set_csvfile_name(area_kor, store_type_kor, 'after'), 
                                 set_xlsxfile_name(area_kor, store_type_kor, 'after'))
                    print(f'{area_kor} 데이터처리 성공')
                except:
                    print(f'{area_kor} 데이터처리 실패')
        return
    
    def one(self, area_kor):
        for store_type_kor in store_type_k_to_e.keys():
            try:
                naver_crawler(area_kor, store_type_kor)
                #? 엑셀에 데이터 저장
                csv_to_excel(set_csvfile_name(area_kor, store_type_kor, 'before'),
                             set_xlsxfile_name(area_kor, store_type_kor, 'before'))
                print(f'{area_kor} 크롤링 성공')
            except:
                print(f'{area_kor} 크롤링 실패')
        
            try:
                processed_data_to_csv(area_kor, 
                                    set_csvfile_name(area_kor, store_type_kor, 'before'), 
                                    set_csvfile_name(area_kor, store_type_kor, 'after'))
                csv_to_excel(set_csvfile_name(area_kor, store_type_kor, 'after'), 
                             set_xlsxfile_name(area_kor, store_type_kor, 'after'))
                print(f'{area_kor} 데이터처리 성공')
            except:
                print(f'{area_kor} 데이터처리 실패')
        return
    
