# SimYaSikDang : 심야 식당 (미니프로젝트: 웹서비스 제작)

## 프로젝트 소개
늦은 시간까지 영업중인 식당과 술집에 대한 정보를 알려주는 웹서비스로 늦은 밤 갈 식당과 술집을 찾는 사람들에게 유용하다.   

## 크롤링
* 주소: 네이버 지도(https://map.naver.com)
- 검색명: ㅁㅁ동 술집 (서울의 유명 동)
* 크롤링 항목: 장소명, 장소 종류, 별점, 총 리뷰 수, 도로명 주소, 영업시간
- 주기: 같은 동에 대해 매주 or 2주마다 (예정) 크롤링 진행하여 db의 장소 데이터를 최신으로 업데이트 예정
* 네이버 api로 경도,위도 가져오는 것과 카카오 api로 지번 주소 가져오는 것은 업데이트할 때 새로 추가되는 장소들에만 적용하여 api가 쓸 데 없이 호출되는 것을 방지한다.

## 메인 페이지
- 시간 필터 사용 시 현재도 열려있고, 그 시간 뒤까지도 열려있는 식당/술집의 정보들이 나온다.
* 탭의 나의 즐겨찾기 클릭 시 내가 좋아요한 식당들이 나온다.
- 장소 이름 클릭 시 네이버 플레이스 URL로 이동한다.
* 길찾기 클릭 시 목적지가 장소인 카카오 길칮기 URL로 이동한다.
- 창크기에 따라 폰트 크기 변화
* 새벽 6시를 기준으로 영업시간 요일 변화 (예를 들어 월요일 오전 3시에 웹사이트에 들어왔을 때 월요일 가게의 운영시간이 아닌 일요일부터 이어진 운영시간을 보는 것이 더 옳기 때문에)

## Tech
- Language : Python
* Web Crawling : Selenium
- Web : Flask, Jinja2 Template, HTML, CSS, Javascript
* DB : Sqlite3
- Environment : VSC, Mac OS

##### TODO : 심야카페 만들기