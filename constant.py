SECRET_KEY = "simyasikdang"
NULL = '정보 없음'
#? 출처: https://www.seoul.go.kr/seoul/autonomy_sub.do
#? 서울의 모든 동
area_dict_ver1 = {
    '강남구': ['신사동', '압구정', '청담동', '삼성동', '대치동', '역삼동', 
            '도곡동', '개포동', '일원동', '수서동', '세곡동']}
#? 내가 생각하는 인기 동
area_dict_ver2 = {
    '강남구': ['신사동', '압구정', '청담동', '삼성동', '대치동', '역삼동', '도곡동'],
    '강동구': ['천호동', '길동'],
    '강북구': ['미아동', '수유동', '우이동'],
    '강서구': ['염창동', '등촌동','발산동'],
    '마포구': ['망원', '상암동', '서교동', '아현동', '연남동', '합정', '홍대'],
    '서대문구':['신촌', '연희동', '가좌동'],
    '경기도 고양시': ['일산'],
    '경기도 수원시': ['수원'],
    '경기도 용인시': ['용인']}
#? 테스트 지역
area_dict = {
    '강남구': ['역삼동'],
    '마포구': ['망원', '연남동', '합정', '홍대'],
    '서대문구':['신촌', '연희동'],
    '경기도 고양시': ['일산']
    }
#? ㄱㄴㄷ 순
area_k_to_e = {
    '망원': 'mangwon',
    '신사동':'sinsadong',
    '신촌': 'sinchon',
    '연남동': 'yeonnamdong',
    '연희동': 'yeonhuidong',
    '역삼동': 'yeoksamdong',
    '일산': 'ilsan',
    '합정': 'hapjeong',
    '홍대': 'hongdae'
    }

store_type_k_to_e = {
    '술집' : 'pub'
}

def set_csvfile_name(area_kor, store_type_kor, status):
    if status == "before":
        return f'./csv/{area_k_to_e[area_kor]}_{store_type_k_to_e[store_type_kor]}_before.csv'
    elif status == "after":
        return f'./csv/{area_k_to_e[area_kor]}_{store_type_k_to_e[store_type_kor]}_after.csv'
    
def set_xlsxfile_name(area_kor, store_type_kor, status):
    if status == "before":
        return f'./excel/{area_k_to_e[area_kor]}_{store_type_k_to_e[store_type_kor]}_before.xlsx'
    elif status == "after":
        return f'./excel/{area_k_to_e[area_kor]}_{store_type_k_to_e[store_type_kor]}_after.xlsx'