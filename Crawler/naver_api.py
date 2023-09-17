import urllib.request
import urllib.parse
import json
from secret import NAVER_REST_API_CLIENT_SECRET, NAVER_MAP_CLIENT_ID, NAVER_MAP_CLIENT_SECRET
import requests

def naver_api_search_info(query="식껍 종로익선점"):
    encText = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/local?query=" + encText
    print(url)

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", 'CEtfT8cBlzYrf6kqToZ2')
    request.add_header("X-Naver-Client-Secret", NAVER_REST_API_CLIENT_SECRET)

    response = urllib.request.urlopen(request)

    response_data = response.read().decode('utf-8')
    data = json.loads(response_data)

    if 'items' in data:
        total_results = data['total']
        for item in data['items']:
            print(item)
            print("이름:", item['title'])
            print("주소:", item['address'])
            print("카테고리:", item['category'])
            print(item['mapx'], item['mapy'])


def naver_map_LatLng(query):
    endpoint = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    url = f"{endpoint}?query={query}"
    # 헤더
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_MAP_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVER_MAP_CLIENT_SECRET,
    }
    # 요청
    res = requests.get(url, headers=headers)
    json = res.json()
    lat = json['addresses'][0]['x']
    lng = json['addresses'][0]['y']
    # print(lat, lng)
    return lat, lng
