import time
import json

from io import TextIOWrapper
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# 크롬 드라이버 실행
def get_driver():
  options = webdriver.ChromeOptions()
  # 지정한 user-agent로 설정
  options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664 Safari/537.36") 
  # 크롬 화면 크기를 설정(but 반응형 사이트에서는 html요소가 달라질 수 있음)
  options.add_argument("window-size=1440x900")
  # 브라우저가 백그라운드에서 실행됩니다.
  # options.add_argument("headless")

  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)  # chromedriver 열기
#   driver = webdriver.Chrome("./chromedriver")
  driver.get('https://map.naver.com')  # 주소 가져오기
  driver.implicitly_wait(60)
  return driver

# 검색어 입력
def search_place(driver:WebDriver, search_text: str):
  search_input_box = driver.find_element_by_css_selector("div.input_box>input.input_search")
  search_input_box.send_keys(search_text)
  search_input_box.send_keys(Keys.ENTER)
  time.sleep(5)

# 다음 페이지 이동 및 마지막 페이지 검사
def next_page_move(driver:WebDriver):
  # 페이지네이션 영역에 마지막 버튼 선택
  next_page_btn = driver.find_element_by_css_selector('div.zRM9F>a:last-child')
  next_page_class_name = BeautifulSoup(next_page_btn.get_attribute('class'), "html.parser")

  if len(next_page_class_name.text) > 10:
    print("검색완료")
    driver.quit()
    return False
  else:
    next_page_btn.send_keys(Keys.ENTER)
    return True

# 검색 iframe 이동
def to_search_iframe(driver:WebDriver):
  driver.switch_to.default_content()
  driver.switch_to.frame('searchIframe')

# element 텍스트 추출
def get_element_to_text(element):
  return BeautifulSoup(element, "html.parser").get_text()

# 매장정보 추출
def get_store_data(driver:WebDriver, scroll_container: WebElement, file: TextIOWrapper):
  # 현재 페이지 매장 리스트
  get_store_li = scroll_container.find_elements_by_css_selector('#_pcmap_list_scroll_container > ul > li')
  
  for index in range(len(get_store_li)):
    # json 파일 저장 init
    # 매장 이름, 네이버 카테고리, 주소, url, 메인 사진 url, 가격, 시간, 레벨, 바뀌는 주기
    climing_info = {}
    store_name = naver_category = address = naver_map_url = main_img_url = ''
    price_list, open_time_list, level_list, change_time_list = [], [], [], []
    
    selectorArgument = 'div:nth-of-type(1) > div.ouxiq > a:nth-child(1)'
    wrapper_html = get_store_li[index].get_attribute('innerHTML')
    wrapper_soup = BeautifulSoup(wrapper_html, "html.parser")

    # 매장 항목 클릭
    get_store_li[index].find_element_by_css_selector(selectorArgument).click()

    # 매장 상세로 iframe 이동
    driver.switch_to.default_content()
    driver.switch_to.frame('entryIframe')

    time.sleep(3)

    try:
      try: 
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, "place_didmount")))
      except TimeoutException:
        to_search_iframe(driver)
        
      # 매장 이름, 네이버 카테고리, 주소, url, 메인 사진 url, 가격, 시간, 레벨, 바뀌는 주기
      # store_name, naver_category, address, naver_map_url, main_img_url, price_list, open_time_list, level_list, change_time_list
      
      # store_name
      try:
        store_name = driver.find_element_by_css_selector('#_title > span:nth-child(1)').get_attribute('innerHTML')
        store_name = get_element_to_text(store_name)
      except:
        pass
      

      # 네이버 카테고리
      try:
        if driver.find_element_by_css_selector('#_title > span:nth-child(2)').is_displayed():
            naver_category = driver.find_element_by_css_selector('#_title > span:nth-child(2)').get_attribute('innerHTML')
        else:
            pass
        naver_category = get_element_to_text(naver_category)
      except:
        pass
      
      
      # 주소
      try:
        address = driver.find_element_by_css_selector('div > a > span.LDgIH').get_attribute('innerHTML')
        address = get_element_to_text(address)
      except:
        pass
      
      # url
      try:
        naver_map_url = driver.current_url
      except:
        pass
      
      # 메인 사진 url
      try:
        tmp = str(wrapper_soup)
        main_img_url = tmp.split('src="')[1].split('"')[0]
      except:
        pass
      
      
      # 가격
      try:
        price_li_elements = driver.find_elements_by_css_selector('div.O8qbU.tXI2c > div > ul > li')
        price_li_text = [element.text for element in price_li_elements]
        for i in price_li_text:
            tmp = i.replace("\n", "=").replace(",000원", "000")
            price_list.append(tmp)
      except:
        price_list = []
      
      # 시간
      try:
        driver.find_element_by_css_selector('div.O8qbU.pSavy > div > a').click()
        time.sleep(1)
        time_li_elements = driver.find_elements_by_css_selector('div.O8qbU.pSavy > div > a > div')
        time_li_text = [element.text for element in time_li_elements]
        for i in time_li_text:
            tmp = i.replace("\n", "=").replace("=접기", "")
            open_time_list.append(tmp)
        open_time_list.pop(0)
      except:
          open_time_list = []
          
      
      # 레벨
      # 네이버지도에서 크롤링 불가능
      # 바뀌는 주기
      # 네이버지도에서 크롤링 불가능
      
      
      
      climing_info = {'store_name': store_name, 'naver_category': naver_category, 'address': address, 'naver_map_url': naver_map_url, 'main_img_url': main_img_url, 'price_list': price_list, 'open_time_list': open_time_list, 'level_list': level_list, 'change_time_list': change_time_list}
      print('-'*15)
      print(climing_info)
      print('\n'*5)
      json_data['climing_list'].append(climing_info)
      
      with open('list.json', 'w') as f:
          json.dump(json_data, f, ensure_ascii=False, indent=4)
      to_search_iframe(driver)
    except TimeoutException:
      to_search_iframe(driver)

# 메인 함수
def naver_crawl():
  with open('./list.json', 'r', encoding="UTF-8") as json_file:
      filer = json.load(json_file)
      json_data = filer
#   filer = open('./list.json','a',encoding='utf-8')
  driver = get_driver()
  search_place(driver,'클라이밍')
  to_search_iframe(driver)
  time.sleep(2)

  try:
    scroll_container = driver.find_element_by_id("_pcmap_list_scroll_container")
  except:
    print("스크롤 영역 감지 실패")

  try:
    while True:
      # 스크롤 내리는 자바 스크립트 코드 실행
      for i in range(6):
        driver.execute_script("arguments[0].scrollBy(0,2000)",scroll_container)
        time.sleep(1)
      get_store_data(driver,scroll_container,filer)
      is_continue = next_page_move(driver)
      if is_continue == False:
        break
  except:
    print("크롤링 과정 중 에러 발생")

# init
json_data = {}
json_data['climing_list'] = []
naver_crawl()