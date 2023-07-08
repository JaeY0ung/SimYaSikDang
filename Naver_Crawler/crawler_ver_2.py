from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib3.util.retry import Retry
import time
import csv


areas = ["홍대", "신촌", "강남", "일산"]
null = "정보 없음"

def naver_crawler(area):
    # chrome_crawler 설정
    chrome_options = Options() # 브라우저 꺼짐 방지
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #불필요한 에러 메세지 삭제
    service = Service(executable_path = ChromeDriverManager().install()) # 크롬 드라이버 최신 버전 자동 설치 후 서비스 만들기
    crawler = webdriver.Chrome(service = service, options = chrome_options)
    main_url = f'https://map.naver.com/v5/search/{area}%20술집/place'

    # 크롤링할 url로 이동
    crawler.get(main_url) # 웹페이지 해당 주소 이동
    crawler.implicitly_wait(3) # 로딩이 끝날동안 기다리기

    # 프레임 이동
    searchIframe = crawler.find_element(By.ID, 'searchIframe')
    crawler.switch_to.frame(searchIframe)
    crawler.implicitly_wait(2) # 로딩이 끝날동안 기다리기

    crawler.find_element(By.CLASS_NAME, "CHC5F").click()
    time.sleep(3)

    # # 페이지의 맨 밑까지 스크롤 (50 ~ 55개 상점 정보) 
    # for _ in range(6):
    #     body = crawler.find_element(By.CSS_SELECTOR, 'body')
    #     body.send_keys(Keys.PAGE_DOWN)
    #     body.send_keys(Keys.PAGE_DOWN)
    #     body.send_keys(Keys.PAGE_DOWN)
    #     body.send_keys(Keys.PAGE_DOWN)
    #     body.send_keys(Keys.PAGE_DOWN)
    #     body.send_keys(Keys.PAGE_DOWN)
    #     h = crawler.execute_script("return document.body.scrollHeight")
    #     # print(f"현재 브라우저 높이: {h}") -> 같게 나옴
    #     time.sleep(1)

    # shop들의 목록이 들어있는 className 찾기
    shops = crawler.find_elements(By.CLASS_NAME, 'UEzoS.rTjJo')
    crawl_data = []
    for shop in shops:
        # frame 밖으로 나가기
        crawler.switch_to.default_content()

        # searchIframe 찾아 들어오기
        searchIframe = crawler.find_element(By.ID, 'searchIframe')
        crawler.switch_to.frame(searchIframe)

        # 가게 명
        shop_name = shop.find_element(By.CLASS_NAME, 'place_bluelink.TYaxT').text
        print(f'가게명: {shop_name}')

        # 가게 종류
        try:
            shop_type = shop.find_element(By.CLASS_NAME, 'KCMnt').text
        except:
            shop_type = null
        print(f'가게 종류: {shop_type}')

        crawler.implicitly_wait(1)

        # 가게명 클릭하여 세부창 띄우기
        shop.find_element(By.CLASS_NAME, 'place_bluelink.TYaxT').click()

        crawler.implicitly_wait(1)
        
        # frame 밖으로 나가기
        crawler.switch_to.default_content()

        # entryIframe 찾아 들어오기
        entryIframe = crawler.find_element(By.ID, 'entryIframe')
        crawler.switch_to.frame(entryIframe)
        time.sleep(1) # 왜인지는 모르지만 crawler.implicitly_wait(5) 쓰면 안된다고 함

        # 가게 별점
        try:
            shop_star_rating = crawler.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div.place_section.OP4V8 > div.zD5Nm.f7aZ0 > div.dAsGb > span.PXMot.LXIwF > em').text
        except:
            shop_star_rating = null
        print(f'별점: {shop_star_rating}')

        # 가게 주소
        try:
            shop_address = crawler.find_element(By.CLASS_NAME, 'LDgIH').text
        except:
            shop_address = null
        print(f'주소: {shop_address}')

        # 가게 영업시간 클릭
        crawler.find_element(By.CLASS_NAME, 'gKP9i.RMgN0').click()
        time.sleep(1)

        # 가게 요일별 영업시간
        time_info = crawler.find_elements(By.CLASS_NAME,'w9QyJ')
        time_info = [element.text for element in time_info]
        shop_time_info = []
        for day_info in time_info:
            day_info = day_info.replace("\n", "=").replace("=접기", "").split('=')
            shop_time_info.append(day_info)
        print(f"영업시간 정보={shop_time_info}")

        # 가게 연락처
        try:
            shop_contact = crawler.find_element(By.CLASS_NAME,'xlx7Q').text
        except:
            shop_contact = null
        print(f'연락처: {shop_contact}')

        row = [shop_name, shop_type, shop_star_rating, shop_address, shop_time_info, shop_contact]
        crawl_data.append(row)

    with open(f'./csv/{area}술집.csv', 'w', encoding= 'UTF-8') as file:
        csvWriter = csv.writer(file)
        csvWriter.writerow(['shop_name', 'shop_type', 'shop_star_rating', 'shop_address', 'shop_time_info', 'shop_contact'])
        for row in crawl_data:
            csvWriter.writerow(row)

# 지역별 크롤링 시작
for area in areas:
     naver_crawler(area)