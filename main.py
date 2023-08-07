from Data_Crawl_and_Process import Data_Crawl_and_Process
from constant import area_k_to_e

if __name__ == '__main__':
    data_processor = Data_Crawl_and_Process()
    print('어느 지역을 가져올까요? (전부: 0)')
    select_area = input()
    if select_area == '0':
        print('모든 지역 크롤링 시작')
        data_processor.all()
    else: 
        if select_area in area_k_to_e.keys():
            print(f'{select_area} 크롤링 시작')
            data_processor.one(select_area)
        else:
            print('잘못 입력했습니다.')