from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import csv
from .constant import dict_area_kor_to_eng, dict_searchtype_to_code, NULL

# ? 페이지의 맨 밑까지 스크롤 (맥 + 34인치 모니터 기준/ 한페이지에 55개 상점 정보)
def scroll_down(crawler):
    for _ in range(10):
        body = crawler.find_element(By.CSS_SELECTOR, "body")
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    return

def naver_crawler(area_kor, place_type_kor="가볼만한곳"):
    start_time = time.time()  # !현재 시각
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #! chrome_crawler 설정
    chrome_options = Options()  # !브라우저 꺼짐 방지
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  #! 불필요한 에러 메세지 삭제
    service = Service(executable_path=ChromeDriverManager().install())  #! 크롬 드라이버 최신 버전 자동 설치 후 서비스 만들기
    crawler = webdriver.Chrome(service=service, options=chrome_options)
    main_url = 'https://map.naver.com/p?c=15.00,0,0,0,dh'

    #! 크롤링할 url로 이동
    crawler.get(main_url)  #! 웹페이지 해당 주소 이동
    time.sleep(5)  #! 로딩이 끝날동안 기다리기
    print('페이지 로딩 완료')

    #! 검색어 입력
    search_input = crawler.find_element(By.CLASS_NAME, 'input_search')
    search_input.send_keys(f"{area_kor} {place_type_kor}")
    search_input.send_keys(Keys.ENTER)
    time.sleep(5)  #! 로딩이 끝날동안 기다리기

    #! 크롤링한 상점들의 정보를 담는 리스트
    crawl_data = []

    # ? 실제 클릭할 페이지: range(1,6) - 5페이지 / 테스트: range(1,2)
    for page in range(1, 2):
        # ! default 창으로 빠져 나오기
        crawler.switch_to.default_content()
        # ! 프레임 이동
        searchIframe = crawler.find_element(By.ID, "searchIframe")
        crawler.switch_to.frame(searchIframe)
        crawler.implicitly_wait(2)  #! 로딩이 끝날동안 기다리기

        #! page 클릭하여 이동
        crawler.find_element(By.CSS_SELECTOR,f"#app-root > div > div.XUrfU > div.zRM9F > a:nth-child({page})").click()
        print(f'페이지 이동 to {page}')

        #! 스크롤 가능하도록 body 중 아무 동작 없는 곳 클릭
        try:
            crawler.find_element(By.ID, "_pcmap_list_scroll_container").click()
        except:
            pass
        crawler.implicitly_wait(2)

        #? 잠시 꺼둠
        #! 페이지의 맨 밑까지 스크롤
        # scroll_down(crawler)

        #! shop들의 목록이 들어있는 className 찾기
        shops = crawler.find_element(By.ID, "_pcmap_list_scroll_container").find_elements(By.TAG_NAME, 'li')
        print(f'총 {len(shops)}개의 장소 찾음')

        #! 가게들 정보 크롤링 시작
        for shop in shops:
            print('----------------------')
            #? 가게명 클릭하여 세부창 띄우기
            try:
                title_clickpoint = shop.find_element(By.CLASS_NAME, "place_bluelink") #! 식당,카페,술집
                title_clickpoint.click()
            except:
                pass
            crawler.implicitly_wait(5)
            time.sleep(1)

            crawler.switch_to.default_content()
            #! entryIframe 찾아 들어오기
            entryIframe = crawler.find_element(By.ID, "entryIframe")
            crawler.switch_to.frame(entryIframe)
            crawler.implicitly_wait(5)
            time.sleep(1)


            #! 이름, 종류
            try:
                title = crawler.find_element(By.ID, '_title')
                title_span = title.find_elements(By.TAG_NAME, 'span')
                name = title_span[0].text
                type = title_span[1].text
            except:
                name, type = NULL, NULL
            print(f'이름: {name}')
            print(f'종류: {type}')
            crawler.implicitly_wait(3)


            #! 별점 + 방문자리뷰 + 블로그리뷰수
            try:
                dAsGb = crawler.find_element(By.CLASS_NAME, 'dAsGb')
                try:
                    star_rating = dAsGb.find_element(By.CLASS_NAME, 'LXIwF').find_element(By.TAG_NAME, 'em').text
                except:
                    star_rating = NULL
                try:
                    review_a_tags = dAsGb.find_elements(By.TAG_NAME, 'a')
                    review_sum = 0
                    for review_a_tag in review_a_tags:
                        review_sum += int(review_a_tag.find_element(By.TAG_NAME, 'em').text)
                except:
                    review_sum = NULL
            except:
                star_rating, review_sum = NULL, NULL
            print(f'별점: {star_rating}   리뷰수: {review_sum}')
            crawler.implicitly_wait(3)


            #! 가게 주소
            try:
                address = crawler.find_element(By.CLASS_NAME, "LDgIH").text
            except:
                address = NULL
            print(f'주소: {address}')
            crawler.implicitly_wait(3)


            #! 가게 연락처
            try:
                contact = crawler.find_element(By.CLASS_NAME, "xlx7Q").text
            except:
                contact = NULL
            print(f'연락처: {contact}')
            crawler.implicitly_wait(3)


            #! 영업시간 펼쳐보기 클릭
            try:
                # crawler.find_element(By.CLASS_NAME, "gKP9i.RMgN0").click()
                crawler.find_element(By.TAG_NAME, "time").click()
            except:
                print(f"{name}의 영업시간 펼쳐보기 클릭 실패")
            #! 가게 영업시간
            try:
                #! 가게 요일별 영업시간
                elements = crawler.find_elements(By.CLASS_NAME,'w9QyJ')
                                                         
                days_opening_hours = [element.text for element in elements]
                opening_hours = []
                for day_info in days_opening_hours:
                    day_info = day_info.replace("\n", "=").replace("=접기", "").split('=')
                    opening_hours.append(day_info)
                
                if len(opening_hours) <= 1:
                    print(f'{name}의 영업시간 정보 못 가져옴 : {opening_hours}')
            except:
                opening_hours = NULL
            crawler.implicitly_wait(2)
            print(opening_hours)
            


            #! url
            try:
                url = crawler.find_element(By.ID, 'og:url').get_attribute('content')
            except:
                url = NULL
            print(f'url: {url}')
            crawler.implicitly_wait(3)

            crawler.switch_to.default_content()
            #! searchIframe 찾아 들어오기
            searchIframe = crawler.find_element(By.ID, "searchIframe")
            crawler.switch_to.frame(searchIframe)
            crawler.implicitly_wait(2)
            time.sleep(1)

            keys   = ["name", "type", "star_rating", "review_sum", "address", "contact", "url", "create_time", "opening_hours"]
            values = [ name ,  type ,  star_rating ,  review_sum ,  address ,  contact ,  url ,  create_time ,  opening_hours ]
            crawl_data.append(dict(zip(keys, values)))

    crawler.quit()
    print(f'크롤링 끝')

    end_time = time.time()  #! 끝난 시간
    print(f"크롤링에 걸린 시간: {(int(end_time - start_time)//60)}분 {(int(end_time - start_time))%60}초")

    with open(f"./crawler/csv/{dict_area_kor_to_eng[area_kor]}_{dict_searchtype_to_code[place_type_kor]}.csv", "w", encoding="UTF-8") as file:
        csvWriter = csv.DictWriter(file, fieldnames=keys)
        csvWriter.writeheader()
        csvWriter.writerows(crawl_data)
    
    print(f'{area_kor} {place_type_kor} 크롤링 & 데이터 저장 성공')