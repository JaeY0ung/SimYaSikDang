from naver_crawler.crawler_ver_2 import naver_crawler
from FileTransform import csv_to_excel, load_csv
import seoul_area_data
from DataProcesing import processed_data_to_csv
from flask import Flask, render_template

areas_dict = seoul_area_data.areas_dict_test

# # 데이터 크롤링하여 csv파일과 엑셀파일로 저장
# for gu, dong in areas_dict.items():
#     for area in dong:
#         naver_crawler(area)
#         csv_to_excel(f"./csv/{area}.csv", f"./excel/{area}.xlsx")  # 엑셀에 데이터 저장

# # 영업시간 데이터 처리하여 csv 파일과 엑셀파일로 저장
# for gu, dong in areas_dict.items():
#     for area in dong:          
#         processed_data_to_csv(area)
#         csv_to_excel(f"./csv/{area}_processed.csv", f"./excel/{area}_processed.xlsx")
    
# areas_csvdata = {
#     '마포구': {'망원' : "./csv/망원_processed.csv", 
#             '연남동' : "./csv/연남동_processed.csv", 
#             '합정' : "./csv/합정_processed.csv", 
#             '홍대' : "./csv/홍대_processed.csv"},
#     '서대문구':{'신촌' : "./csv/신촌_processed.csv"},
#     '경기도': {'일산' : "./csv/망원_processed.csv"}
# }
# for gu in areas_csvdata.keys():
#     for area in areas_csvdata[gu].keys():
#         csvfile = areas_csvdata[gu][area]


# TODO: 일단 하나의 지역(망원)의 술집 관련 페이지 제작
# TODO: 이후 모든 지역마다 페이지 생성

data = load_csv("./csv/망원_processed.csv")
print(data)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html", data=data)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)