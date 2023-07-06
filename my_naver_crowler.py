from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains # ActionChains 를 사용하기 위해서.
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import time
import pandas as pd
import csv
import datetime
import re
import requests

area_and_types = ["신촌 술집", "강남 술집", "일산 술집"]

def naver_crawler(area_and_type):
    search_area = area_and_type.split()[0]
    search_type = area_and_type.split()[1]
    chrome_options = Options() #브라우저 꺼짐 방지
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #불필요한 에러 메세지 삭제

    service = Service(executable_path = ChromeDriverManager().install()) # 크롬 드라이버 최신 버전 자동 설치 후 서비스 만들기
    crawler = webdriver.Chrome(service = service, options = chrome_options)
    main_url = f'https://map.naver.com/v5/search/{search_area}%20{search_type}/place'

    crawler.get(main_url) #웹페이지 해당 주소 이동

    crawler.implicitly_wait(3)
    searchIframe = crawler.find_element(By.ID, 'searchIframe')
    crawler.switch_to.frame(searchIframe)

    crawler.implicitly_wait(3) #로딩이 끝날동안 기다리기

    with open(f'{search_area}{search_type}_shopdata.csv', 'w',encoding= 'UTF-8') as f:
        csvWriter = csv.writer(f)
        
        # TODO: 
        # 브라우저 끝까지 내리기
        for _ in range(30):
            body = crawler.find_element(By.CSS_SELECTOR, 'body')
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
        # while True:
        #     before_h = crawler.execute_script("return document.body.scrollHeight") # 브라우저 상의 처음 높이
        #     print(f"before_h={before_h}") 
        #     time.sleep(10) # 화면 켜질 때 시간이 좀 걸리기 때문에
        #     crawler.execute_script("window.scrollTo(0, document.body.scrollHeight)") # 스크롤 내리기
        #     time.sleep(10) # 검색결과 뜰 때까지 기다리기 위해
        #     after_h = crawler.execute_script("return document.body.scrollHeight")
        #     if after_h == before_h:
        #         break
        #     before_h = after_h


        shops = crawler.find_elements(By.CLASS_NAME, 'UEzoS.rTjJo')
        for shop in shops:
            # frame 밖으로 나가기
            crawler.switch_to.default_content()
            # searchIframe 찾아 들어오기
            searchIframe = crawler.find_element(By.ID, 'searchIframe')
            crawler.switch_to.frame(searchIframe)

            # 가게명 가져오기
            shop_name = shop.find_element(By.CLASS_NAME, 'place_bluelink.TYaxT').text
            # 가게 카테고리 가져오기
            shop_type = shop.find_element(By.CLASS_NAME, 'KCMnt').text
            # 가게명 클릭하여 세부창 띄우기
            shop.find_element(By.CLASS_NAME, 'place_bluelink.TYaxT').click()
            
            crawler.implicitly_wait(1)
            # frame 밖으로 나가기
            crawler.switch_to.default_content()
            # entryIframe 찾아 들어오기
            entryIframe = crawler.find_element(By.ID, 'entryIframe')
            crawler.switch_to.frame(entryIframe)

            # 왜인지는 모르지만 crawler.implicitly_wait(5) 쓰면 안된다고 함
            time.sleep(2)

            crawler.find_element(By.CLASS_NAME, 'gKP9i.RMgN0').click()
            time.sleep(1)

            shop_time_crawling = crawler.find_elements(By.CLASS_NAME,'gKP9i.RMgN0')
            shop_time_info = [element.text for element in shop_time_crawling]
            print(f"shop_time_info={shop_time_info}")
            open_time_info = []
            for day in shop_time_info:
                tmp = day.replace("\n", "=").replace("=접기", "").split('=')
                open_time_info.append(tmp)
            
            csvWriter.writerow([shop_name, shop_type, open_time_info])

for area_and_type in area_and_types:
     naver_crawler(area_and_type)