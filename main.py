from naver_crawler.crawler_ver_2 import naver_crawler
from csv_to_excel import csv_to_excel, csv_to_excel_2
import areas_info
from data_processing import processed_data_to_csv
from flask import Flask, render_template

# areas_dict = areas_info.areas_dict_ver2
areas_dict = areas_info.areas_dict_test

if input("data를 생성하시겠습니까?(Y/N): ").lower() == 'y':
    for gu, dong in areas_dict.items():
        for area in dong:
            naver_crawler(area) # 크롤링
            csv_to_excel(area)  # 엑셀에 데이터 저장
            processed_data_to_csv(area) # 데이터 처리하여 csv 파일에 저장
            csv_to_excel_2(area)  # 엑셀에 데이터 저장


# 웹 페이지
# app = Flask(__name__)
# app.route('/')
# def home():
#     return render_template('home.html')

# if __name__ == '__main__':
#     app.run('0.0.0.0', port=8080, debug=True)