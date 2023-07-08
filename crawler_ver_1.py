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

areas = ["홍대", "신촌", "강남", "일산", "연남동"]
type = "술집"

def naver_crawler(area, type):
    # chrome_crawler 설정
    chrome_options = Options() # 브라우저 꺼짐 방지
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #불필요한 에러 메세지 삭제
    service = Service(executable_path = ChromeDriverManager().install()) # 크롬 드라이버 최신 버전 자동 설치 후 서비스 만들기
    crawler = webdriver.Chrome(service = service, options = chrome_options)
    main_url = f'https://map.naver.com/v5/search/{area}%20{type}/place'

    # 크롤링할 url로 이동
    crawler.get(main_url) # 웹페이지 해당 주소 이동
    crawler.implicitly_wait(3) # 로딩이 끝날동안 기다리기

    # 프레임 이동
    searchIframe = crawler.find_element(By.ID, 'searchIframe')
    crawler.switch_to.frame(searchIframe)
    crawler.implicitly_wait(2) # 로딩이 끝날동안 기다리기

    with open(f'{area}{type}_shopdata.csv', 'w', encoding= 'UTF-8') as f:
        csvWriter = csv.writer(f)
        crawler.find_element(By.CLASS_NAME, "CHC5F").click()
        time.sleep(3)
        # 페이지의 맨 밑까지 스크롤 (50 ~ 55개 상점 정보) 
        for _ in range(12):
            body = crawler.find_element(By.CSS_SELECTOR, 'body')
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            h = crawler.execute_script("return document.body.scrollHeight")
            print(f"현재 브라우저 높이: {h}")
            time.sleep(1)

        # shop들의 목록이 들어있는 className 찾기
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
            print(f"open_time_info={open_time_info}")
            for day in shop_time_info:
                tmp = day.replace("\n", "=").replace("=접기", "").split('=')
                open_time_info.append(tmp)
            
            csvWriter.writerow([shop_name, shop_type.strip('"'), open_time_info])
            print(shop_name, shop_type, open_time_info)

# 지역별 크롤링 시작
for area in areas:
     naver_crawler(area, type)