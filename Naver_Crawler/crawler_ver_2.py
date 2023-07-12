from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

# 페이지의 맨 밑까지 스크롤 (50 ~ 55개 상점 정보)
def scroll_down(crawler):
    for _ in range(10):
        body = crawler.find_element(By.CSS_SELECTOR, 'body')
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    return

def naver_crawler(area):
    null = "정보 없음"

    # chrome_crawler 설정
    chrome_options = Options() # 브라우저 꺼짐 방지
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #불필요한 에러 메세지 삭제
    service = Service(executable_path = ChromeDriverManager().install()) # 크롬 드라이버 최신 버전 자동 설치 후 서비스 만들기
    crawler = webdriver.Chrome(service = service, options = chrome_options)
    main_url = f'https://map.naver.com/v5/search/{area}%20술집/place'

    # 크롤링할 url로 이동
    crawler.get(main_url) # 웹페이지 해당 주소 이동
    crawler.implicitly_wait(5) # 로딩이 끝날동안 기다리기

    # 크롤링한 상점들의 정보를 담는 리스트
    crawl_data = []
    
    for page in range(1,6): # 페이지 클릭수
        # default
        crawler.switch_to.default_content()
        # 프레임 이동
        searchIframe = crawler.find_element(By.ID, 'searchIframe')
        crawler.switch_to.frame(searchIframe)
        crawler.implicitly_wait(2) # 로딩이 끝날동안 기다리기

        # page 클릭하여 이동
        crawler.find_element(By.CSS_SELECTOR, f"#app-root > div > div.XUrfU > div.zRM9F > a:nth-child({page})").click()

        crawler.find_element(By.CLASS_NAME, "CHC5F").click()
        crawler.implicitly_wait(2)

        # 페이지의 맨 밑까지 스크롤
        scroll_down(crawler)

        # shop들의 목록이 들어있는 className 찾기
        shops = crawler.find_elements(By.CLASS_NAME, 'UEzoS.rTjJo')

        # 가게들 정보 크롤링 시작
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

            crawler.implicitly_wait(2)

            # 가게명 클릭하여 세부창 띄우기
            # shop.find_element(By.CLASS_NAME, 'place_bluelink.TYaxT').click()
            shop.find_element(By.CLASS_NAME, 'N_KDL').click()

            crawler.implicitly_wait(1)
            
            # frame 밖으로 나가기
            crawler.switch_to.default_content()
            
            crawler.implicitly_wait(3)

            # entryIframe 찾아 들어오기
            entryIframe = crawler.find_element(By.ID, 'entryIframe')
            crawler.switch_to.frame(entryIframe)

            crawler.implicitly_wait(3)
            # time.sleep(1) # 왜인지는 모르지만 crawler.implicitly_wait(5) 쓰면 안된다고 함

            # 가게 별점
            try:
                shop_star_rating = crawler.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div.place_section.OP4V8 > div.zD5Nm.f7aZ0 > div.dAsGb > span.PXMot.LXIwF > em').text
            except:
                shop_star_rating = null
            print(f'별점: {shop_star_rating}')

            crawler.implicitly_wait(3)

            # 가게 주소
            try:
                shop_address = crawler.find_element(By.CLASS_NAME, 'LDgIH').text
            except:
                shop_address = null
            print(f'주소: {shop_address}')

            crawler.implicitly_wait(3)

            # 가게 영업시간
            try:
                crawler.find_element(By.CLASS_NAME, 'gKP9i.RMgN0').click()
                # time.sleep(1.5)
                crawler.implicitly_wait(3)
                # 가게 요일별 영업시간
                time_info = crawler.find_elements(By.CLASS_NAME,'w9QyJ')
                time_info = [element.text for element in time_info]
                shop_time_info = []
                for day_info in time_info:
                    day_info = day_info.replace("\n", "=").replace("=접기", "").split('=')
                    shop_time_info.append(day_info)
            except:
                shop_time_info = null
            print(f"영업시간 정보: {shop_time_info}")

            crawler.implicitly_wait(1)

            # 가게 연락처
            try:
                shop_contact = crawler.find_element(By.CLASS_NAME,'xlx7Q').text
            except:
                shop_contact = null
            print(f'연락처: {shop_contact}')

            values = ['shop_name', 'shop_type', 'shop_star_rating', 'shop_address', 'shop_time_info', 'shop_contact']
            keys = [shop_name, shop_type, shop_star_rating, shop_address, shop_time_info, shop_contact]
            crawl_data.append(dict(zip(values, keys)))
    
    crawler.quit()

    with open(f'./csv/{area}.csv', 'w', encoding= 'UTF-8') as file:
        csvWriter = csv.DictWriter(file, fieldnames=values)
        csvWriter.writeheader()
        for row in crawl_data:
            csvWriter.writerow(row)
