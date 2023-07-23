from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv
from src.area import k_to_e

# 페이지의 맨 밑까지 스크롤 (맥 + 34인치 모니터 기준/ 한페이지에 55개 상점 정보)
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

# 내 방 네트워크 환경에서 맥북 에어를 이용하여 합정 5페이지 크롤링에 걸린 시간: 12분
def naver_crawler(area):
    null = "정보 없음"
    start_time =  time.time()
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

    #? 실제 클릭할 페이지: range(1,6)
    #? 테스트: range(1,2)
    for page in range(1,6):
        # default
        crawler.switch_to.default_content()
        # 프레임 이동
        searchIframe = crawler.find_element(By.ID, 'searchIframe')
        crawler.switch_to.frame(searchIframe)
        crawler.implicitly_wait(2) # 로딩이 끝날동안 기다리기

        # page 클릭하여 이동
        crawler.find_element(By.CSS_SELECTOR, f"#app-root > div > div.XUrfU > div.zRM9F > a:nth-child({page})").click()

        # 스크롤 가능하도록 body 중 아무 동작 없는 곳 클릭
        crawler.find_element(By.CLASS_NAME, "CHC5F").click()
        crawler.implicitly_wait(2)
        # 페이지의 맨 밑까지 스크롤
        scroll_down(crawler)

        # shop들의 목록이 들어있는 className 찾기
        shops = crawler.find_elements(By.CLASS_NAME, 'UEzoS.rTjJo')
        # 가게들 정보 크롤링 시작
        for shop in shops:
            name, type, star_rating, review_sum, address, time_info, contact = null, null, null, null, null, null, null

            # default 콘텐츠로 이동: frame 밖으로 나가기
            crawler.switch_to.default_content()
            # searchIframe 찾아 들어오기
            searchIframe = crawler.find_element(By.ID, 'searchIframe')
            crawler.switch_to.frame(searchIframe)
            crawler.implicitly_wait(5)

            #? 가게 명
            try:
                name = shop.find_element(By.CLASS_NAME, 'place_bluelink.TYaxT').text
            except:
                name = null
            crawler.implicitly_wait(5)

            #? 가게 종류
            try:
                type = shop.find_element(By.CLASS_NAME, 'KCMnt').text
            except:
                type = null
            crawler.implicitly_wait(5)

            #? 가게명 클릭하여 세부창 띄우기
            shop.find_element(By.CLASS_NAME, 'N_KDL').click()
            crawler.implicitly_wait(5)
        
            #? frame 밖으로 나가기
            crawler.switch_to.default_content()
            #? entryIframe 찾아 들어오기
            entryIframe = crawler.find_element(By.ID, 'entryIframe')
            crawler.switch_to.frame(entryIframe)
            crawler.implicitly_wait(5)
            time.sleep(2)

            #? 영업시간 펼쳐보기 클릭 먼저 해놓기!
            try:
                crawler.find_element(By.CLASS_NAME, 'gKP9i.RMgN0').click()
            except:
                print(f'{name}의 영업시간 펼쳐보기 클릭 실패')

            #? 가게 별점
            try:
                star_rating = crawler.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div.place_section.OP4V8 > div.zD5Nm.f7aZ0 > div.dAsGb > span.PXMot.LXIwF > em').text
            except:
                star_rating = null
            crawler.implicitly_wait(5)

            #? 방문자리뷰 + 블로그리뷰수
            try:
                review_sum = 0
                reviews = crawler.find_elements(By.CSS_SELECTOR, '#app-root > div > div > div > div.place_section.OP4V8 > div.zD5Nm.f7aZ0 > div.dAsGb > span > a > em')
                for review in reviews:
                    review_sum += int(review.text)
            except:
                review_sum = null
            crawler.implicitly_wait(5)
            time.sleep(1)
            
            #? 가게 주소
            try:
                address = crawler.find_element(By.CLASS_NAME, 'LDgIH').text
            except:
                address = null
            crawler.implicitly_wait(5)
            # time.sleep(1)
                         
            #? 가게 영업시간
            try:
                # 가게 요일별 영업시간
                time_crawler = crawler.find_element(By.CLASS_NAME, 'gKP9i.RMgN0')

                elements = time_crawler.find_elements(By.CLASS_NAME,'w9QyJ')
                                                         
                days_time_info = [element.text for element in elements]
                time_info = []
                for day_info in days_time_info:
                    day_info = day_info.replace("\n", "=").replace("=접기", "").split('=')
                    time_info.append(day_info)
                
                if len(time_info) == 1:
                    print(f'{name}의 영업시간 정보 못 가져옴')
            except:
                time_info = null
            crawler.implicitly_wait(5)

            # 가게 연락처
            try:
                contact = crawler.find_element(By.CLASS_NAME,'xlx7Q').text
            except:
                contact = null

            values = ['name', 'type', 'star_rating', 'review_sum', 'address', 'time_info', 'contact']
            keys = [name, type, star_rating, review_sum, address, time_info, contact]
            crawl_data.append(dict(zip(values, keys)))
    
    end_time =  time.time()
    print(f'크롤링에 걸린 시간: {(int(end_time - start_time)//60)}분 {(int(end_time - start_time))%60}초')
    crawler.quit()
    with open(f'./csv/{k_to_e[area]}.csv', 'w', encoding= 'UTF-8') as file:
        csvWriter = csv.DictWriter(file, fieldnames=values)
        csvWriter.writeheader()
        csvWriter.writerows(crawl_data)