# from selenium import webdriver
# from selenium.webdriver.common.by import By


# def test_eight_components():
#     driver = webdriver.Chrome()

#     driver.get("https://www.selenium.dev/selenium/web/web-form.html")

#     title = driver.title
#     assert title == "Web form"

#     driver.implicitly_wait(0.5)

#     text_box = driver.find_element(by=By.NAME, value="my-text")
#     submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

#     text_box.send_keys("Selenium")
#     submit_button.click()

#     message = driver.find_element(by=By.ID, value="message")
#     value = message.text
#     assert value == "Received!"

#     driver.quit()
    
# test_eight_components()

from selenium import webdriver
import chromedriver_autoinstaller
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import shutil

def selenium_test():
    # chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    # print(f"chrome_ver: {chrome_ver}")

    # path = os.path.join(os.getcwd(), chrome_ver)
    # path = os.path.join(path,'chromedriver.exe') # /Users/jeongjaeyeong/Project/MiniProject_SimYaSikDang/114/chromedriver.exe
    # print(f"path: {path}")
    URL = "https://www.naver.com/"

    crawler = webdriver.Chrome()

    crawler.implicitly_wait(10) # timesleep 비슷한 기능: 10초 기다리지만 중간에 완료되면 시작
    crawler.get(url=URL)

    while True:
        pass
selenium_test()




# def doScrollDown(whileSeconds):
#         start = datetime.datetime.now()
#         end = start + datetime.timedelta(seconds=whileSeconds)
#         while True:
#             driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#             time.sleep(1)
#             if datetime.datetime.now() > end:
#                 break

# area_and_types = ["신촌 술집", "강남 술집", "일산 술집"]

# for area_and_type in area_and_types:
#     search_area = area_and_type.split()[0]
#     search_type = area_and_type.split()[1]
#     chrome_options = Options() #브라우저 꺼짐 방지
#     chrome_options.add_experimental_option("detach", True)
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #불필요한 에러 메세지 삭제

#     service = Service(executable_path = ChromeDriverManager().install()) #크롬 드라이버 최신 버전 자동 설치 후 서비스 만들기
#     driver = webdriver.Chrome(service = service, options = chrome_options)
#     before_url = f'https://map.naver.com/v5/search/{search_area}%20{search_type}/place'

#     driver.get(before_url) #웹페이지 해당 주소 이동

#     # iframes = driver.find_elements(By.CSS_SELECTOR,'iframe')
#     # for iframe in iframes:
#     #     print(iframe.get_attribute('name'))

#     driver.switch_to.frame('searchIframe')
#     driver.implicitly_wait(5) #로딩이 끝날동안 기다리기

#     doScrollDown(7)

#     with open(f'{search_area}{search_type}_shopdata.csv', 'w',encoding= 'UTF-8') as f:
#         csvWriter = csv.writer(f)
#         shops = driver.find_elements(By.CSS_SELECTOR, '#_pcmap_list_scroll_container > ul > li')
#         for shop in shops:
#             # driver.switch_to.frame('searchIframe')

#             shop_name = shop.find_element(By.CSS_SELECTOR, '#_pcmap_list_scroll_container > ul > li > div.CHC5F > a.tzwk0 > div > div > span.place_bluelink.TYaxT').text
#             shop_type = shop.find_element(By.CSS_SELECTOR, '#_pcmap_list_scroll_container > ul > li > div.CHC5F > a.tzwk0 > div > div > span.KCMnt').text
#             shop.find_element(By.CSS_SELECTOR, '#_pcmap_list_scroll_container > ul > li > div.CHC5F > a.tzwk0 > div > div > span.place_bluelink.TYaxT').click()

#             # after_url = driver.current_url
#             # driver.get(after_url) #웹페이지 해당 주소 이동
#             driver.switch_to.default_content()
#             driver.switch_to.frame('searchIframe')
#             # print(driver.current_url)

#             shop_time = shop.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div > div > div.place_section.no_margin.vKA6F > div > div > div.O8qbU.pSavy > div > a').click()
#             time.sleep(1)
#             time_li_elements=driver.find_elements(By.CSS_SELECTOR,'#app-root > div > div > div > div > div > div.place_section.no_margin.vKA6F > div > div > div.O8qbU.pSavy > div > a > div')
#             time_li_text = [element.text for element in time_li_elements]

#             open_time_list = []
#             for i in time_li_text:
#                 tmp = i.replace("\n", "=").replace("=접기", "")
#                 open_time_list.append(tmp)
#             open_time_list.pop(0)
#             print(shop_time)               
#             csvWriter.writerow([shop_name, shop_type])