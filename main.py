from Data_Crawl_and_Process import Data_Crawl_and_Process

n_to_k = {'0' : 'all',
        '1' : '역삼동',
        '2' : '망원',
        '3' : '연남동',    
        '4' : '합정',    
        '5' : '홍대',    
        '6' : '신촌'}

if __name__ == '__main__':
    data_processor = Data_Crawl_and_Process()
    print('어느 지역을 가져올까요?')
    print('0.all    1.역삼동    2.망원    3.연남동    4.합정    5.홍대    6.신촌')
    select_num = input()
    if select_num == '0':
        print('모든 지역 크롤링 시작')
        data_processor.all()
    else: 
        try:
            print(f'{n_to_k[select_num]} 크롤링 시작')
            data_processor.one(n_to_k[select_num])
        except:
            print('잘못 입력했습니다.')