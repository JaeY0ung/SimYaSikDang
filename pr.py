from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver import ActionChains # ActionChains 를 사용하기 위해서.
# import re
# import requests
# from urllib3.util.retry import Retry
# from requests.adapters import HTTPAdapter
# from bs4 import BeautifulSoup

driver = webdriver.Chrome("/Users/jeongjaeyeong/anaconda3/lib/python3.10/site-packages/chromedriver")
# chromedriver는 따로 설치를 해서 경로를 지정해줘야한다.
def menu(data): # 메뉴 크롤링
    driver.get("https://map.naver.com/v5/search/"+data) # 검색창에 가게이름 입력
    time.sleep(3)
    driver.implicitly_wait(3)
    # iframes = driver.find_elements_by_css_selector('iframe') # 창에 있는 모든 iframe 출력
    # for iframe in iframes:
    #     print(iframe.get_attribute('id'))
    driver.switch_to.frame('searchIframe') #  검색하고나서 가게정보창이 바로 안뜨는 경우 고려해서 무조건 맨위에 가게 링크 클릭하게 설정
    driver.implicitly_wait(3)
    temp = driver.find_element_by_xpath('//*[@id="_pcmap_list_scroll_container"]/ul') # 메뉴표에 있는 텍스트 모두 들고옴(개발자 도구에서 그때그때 xpath 복사해서 들고오는게 좋다)
    driver.implicitly_wait(20) # selenium에서 가끔씩 태그 시간내에 못찾는 경우 때문에 일부러 길게 설정해놓음
    button = temp.find_elements_by_tag_name('a')
    driver.implicitly_wait(20)
    if '이미지수' in button[0].text or button[0].text == '': # 가게 정보에 사진이 있는경우
        button[1].send_keys(Keys.ENTER) 
    else: # 사진이 없는 경우
        button[0].send_keys(Keys.ENTER)
    driver.implicitly_wait(3)
    time.sleep(3)
    driver.switch_to.default_content()# frame이 이상하게 넘어가는 경우 방지를 위해 원래 frame으로 변경한 후에 이동
    driver.switch_to.frame('entryIframe') # 메뉴정보가 entryIframe에 있기 때문에 frame 변경함
    driver.implicitly_wait(2)
    # time.sleep(3)
    start = driver.find_elements_by_class_name('_3ak_I') # 배달의 민족에서 제공하는 메뉴가 랜더링 되어 있는 경우
    if len(start) == 0: # 가게에서 직접 제공하는 메뉴가 랜더링 되어 있는 경우
        start = driver.find_elements_by_class_name('V1UmJ')
    if len(start) == 0: # 메뉴가 없는 경우
        print('메뉴가 없습니다')
        return -1
    return start[0].text

menu("경북대 베스킨라빈스")