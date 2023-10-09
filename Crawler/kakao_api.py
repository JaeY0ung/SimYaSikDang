from secret import KAKAO_REST_API_KEY
import requests

def get_address(query):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {
        "Authorization": f"KakaoAK { KAKAO_REST_API_KEY }"
    }
    response = requests.get(url, headers=headers, params={"query": query})

    if response.status_code == 200:
        data = response.json()
        #! 지번 주소
        lot_number_address = data['documents'][0]['address']['address_name']
        print(lot_number_address)
        #! 도로명 주소
        # road_address       = data['documents'][0]['road_address']['address_name']
        # print(road_address)
    else:
        print(f"에러 발생: {response.status_code}")