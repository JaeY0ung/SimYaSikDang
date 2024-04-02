from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import csv
from constant import dict_area_kor_to_eng, dict_searchtype_to_code, NULL


class NaverCrawler:
    def __init__(self):
        #! chrome_crawler 설정
        # ChromeDriverManager().install()
        # https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.88/mac-arm64/chromedriver-mac-arm64.zip
        # service = Service('/Users/jeongjaeyeong/.wdm/drivers/chromedriver/mac64/117.0.5938.88/chromedriver-mac-arm64/chromedriver')  #! 크롬 드라이버 최신 버전 자동 설치 후 서비스 생성
        service = Service('./crawler/chromedriver/chromedriver')  #! 크롬 드라이버 최신 버전 자동 설치 후 서비스 생성
        chrome_options = Options()  # !브라우저 꺼짐 방지
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  #! 불필요한 에러 메세지 삭제
        self.crawler = webdriver.Chrome(service=service, options=chrome_options)
        
    # ? 페이지의 맨 밑까지 스크롤 (맥 + 34인치 모니터 기준/ 한페이지에 55개 상점 정보)
    def scroll_down(self):
        for _ in range(10):
            body = self.crawler.find_element(By.CSS_SELECTOR, "body")
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

    def naver_crawler(self, area_kor, place_type_kor):
        start_time  = time.time()  # !현재 시각
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #! 크롤링할 url로 이동
        main_url = 'https://map.naver.com/p?c=15.00,0,0,0,dh'
        self.crawler.get(main_url)  #! 웹페이지 해당 주소 이동
        time.sleep(5)  #! 로딩이 끝날동안 기다리기
        print('페이지 로딩 완료')

        #! 검색어 입력
        search_input = self.crawler.find_element(By.CLASS_NAME, 'input_search')
        search_input.send_keys(f"{area_kor} {place_type_kor}")
        search_input.send_keys(Keys.ENTER)
        time.sleep(5)  #! 로딩이 끝날동안 기다리기

        #! 크롤링한 상점들의 정보를 담는 리스트
        crawl_data = []

        # ? 실제 클릭할 페이지: range(1,6) - 5페이지 / 테스트: range(1,2)
        for page in range(1, 2):
            # ! default 창으로 빠져 나오기
            self.crawler.switch_to.default_content()
            # ! 프레임 이동
            searchIframe = self.crawler.find_element(By.ID, "searchIframe")
            self.crawler.switch_to.frame(searchIframe)
            self.crawler.implicitly_wait(2)  #! 로딩이 끝날동안 기다리기

            #! page 클릭하여 이동
            self.crawler.find_element(By.CSS_SELECTOR,f"#app-root > div > div.XUrfU > div.zRM9F > a:nth-child({page})").click()
            print(f'페이지 이동 to {page}')

            #! 스크롤 가능하도록 body 중 아무 동작 없는 곳 클릭
            try:
                self.crawler.find_element(By.ID, "_pcmap_list_scroll_container").click()
            except:
                pass
            self.crawler.implicitly_wait(2)

            #! 페이지의 맨 밑까지 스크롤
            self.scroll_down()

            #! shop들의 목록이 들어있는 className 찾기
            shops = self.crawler.find_element(By.ID, "_pcmap_list_scroll_container").find_elements(By.TAG_NAME, 'li')
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
                self.crawler.implicitly_wait(5)
                time.sleep(1)

                self.crawler.switch_to.default_content()
                #! entryIframe 찾아 들어오기
                entryIframe = self.crawler.find_element(By.ID, "entryIframe")
                self.crawler.switch_to.frame(entryIframe)
                self.crawler.implicitly_wait(5)
                time.sleep(1)


                #! 이름, 종류
                try:
                    title = self.crawler.find_element(By.ID, '_title')
                    title_span = title.find_elements(By.TAG_NAME, 'span')
                    name = title_span[-2].text # name = title_span[0].text # TODO : '새로오픈'으로 가져와져서 제대로 가져오기
                    type = title_span[-1].text # type = title_span[1].text
                except:
                    name, type = NULL, NULL
                print(f'이름: {name}')
                print(f'종류: {type}')
                self.crawler.implicitly_wait(3)


                #! 별점 + 방문자리뷰 + 블로그리뷰수
                try:
                    dAsGb = self.crawler.find_element(By.CLASS_NAME, 'dAsGb')
                    try:
                        star_rating = dAsGb.find_element(By.CLASS_NAME, 'LXIwF').find_element(By.TAG_NAME, 'em').text
                    except:
                        star_rating = NULL
                    try:
                        review_a_tags = dAsGb.find_elements(By.TAG_NAME, 'a')
                        review_total = 0
                        for review_a_tag in review_a_tags:
                            review_total += int(review_a_tag.find_element(By.TAG_NAME, 'em').text)
                    except:
                        review_total = NULL
                except:
                    star_rating, review_total = NULL, NULL
                print(f'별점: {star_rating}   리뷰수: {review_total}')
                self.crawler.implicitly_wait(3)


                #! 가게 주소
                try:
                    address = self.crawler.find_element(By.CLASS_NAME, "LDgIH").text
                except:
                    address = NULL
                print(f'주소: {address}')
                self.crawler.implicitly_wait(3)


                #! 가게 연락처
                try:
                    contact = self.crawler.find_element(By.CLASS_NAME, "xlx7Q").text
                except:
                    contact = NULL
                print(f'연락처: {contact}')
                self.crawler.implicitly_wait(3)


                #! 영업시간 펼쳐보기 클릭
                try:
                    # self.crawler.find_element(By.CLASS_NAME, "gKP9i.RMgN0").click()
                    self.crawler.find_element(By.TAG_NAME, "time").click()
                except:
                    print(f"{name}의 영업시간 펼쳐보기 클릭 실패")
                #! 가게 영업시간
                try:
                    #! 가게 요일별 영업시간
                    elements = self.crawler.find_elements(By.CLASS_NAME,'w9QyJ')
                                                            
                    days_opening_hours = [element.text for element in elements]
                    opening_hours = []
                    for day_info in days_opening_hours:
                        day_info = day_info.replace("\n", "=").replace("=접기", "").split('=')
                        opening_hours.append(day_info)
                    
                    if len(opening_hours) <= 1:
                        print(f'{name}의 영업시간 정보 못 가져옴 : {opening_hours}')
                except:
                    opening_hours = NULL
                self.crawler.implicitly_wait(2)
                print(opening_hours)


                #! place_url
                try:
                    place_url = self.crawler.find_element(By.ID, 'og:url').get_attribute('content')
                except:
                    place_url = NULL
                print(f'place_url: {place_url}')
                self.crawler.implicitly_wait(3)

                self.crawler.switch_to.default_content()
                #! searchIframe 찾아 들어오기
                searchIframe = self.crawler.find_element(By.ID, "searchIframe")
                self.crawler.switch_to.frame(searchIframe)
                self.crawler.implicitly_wait(2)
                time.sleep(1)

                keys   = ["name", "type", "star_rating", "review_total", "address", "contact", "place_url", "created_at", "opening_hours"]
                values = [ name ,  type ,  star_rating ,  review_total ,  address ,  contact ,  place_url ,  created_at ,  opening_hours ]
                crawl_data.append(dict(zip(keys, values)))

        self.crawler.quit()
        print(f'크롤링 끝')

        end_time = time.time()  #! 끝난 시간
        print(f"크롤링에 걸린 시간: {(int(end_time - start_time)//60)}분 {(int(end_time - start_time))%60}초")

        with open(f"./crawler/csv/{dict_area_kor_to_eng[area_kor]}_{dict_searchtype_to_code[place_type_kor]}.csv", "w", encoding="UTF-8") as file:
            csvWriter = csv.DictWriter(file, fieldnames=keys)
            csvWriter.writeheader()
            csvWriter.writerows(crawl_data)
        
        print(f'{area_kor} {place_type_kor} 크롤링 & 데이터 저장 성공')

    # import multiprocessing
    # def naver_crawler_multi_thread():
    #     cpu_count = multiprocessing.cpu_count()
    #     print ('--- cpu_count ', cpu_count) 
    #     pool = multiprocessing.Pool(2)
    #     pool.map(naver_crawler, [('망원동', '술집'), ('망원동', '카페')])
    #     pool.close()
    #     pool.join()

    #     print(f'모두 크롤링 & 데이터 저장 성공')