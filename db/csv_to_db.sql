- 특정지역 다시 크롤링 했을때:  csv로 만든 기존 테이블 삭제
DROP TABLE hapjeong;
DROP TABLE hongdae;
DROP TABLE mangwon;
DROP TABLE sinchon;
DROP TABLE yeoksamdong;
DROP TABLE yeonhuidong;
DROP TABLE yeonnamdong;
--------------------------------------------------------
- 상점 정보들 최신 크롤링 데이터로 모두 교체할 때: 모든 테이블 삭제
DROP TABLE area;

-csv 파일 db로 저장
.mode csv
.import ../csv/hapjeong_processed.csv hapjeong
.import ../csv/hongdae_processed.csv hongdae
.import ../csv/mangwon_processed.csv mangwon
.import ../csv/sinchon_processed.csv sinchon
.import ../csv/yeoksamdong_processed.csv yeoksamdong
.import ../csv/yeonhuidong_processed.csv yeonhuidong
.import ../csv/yeonnamdong_processed.csv yeonnamdong
--------------------------------------------------------
- id를 가진 table2 생성
CREATE TABLE IF NOT EXISTS restaurants(
"uuid" INTEGER PRIMARY KEY,
"create_time" DATETIME,
"area" TEXT,
"name" TEXT,
"type" TEXT,
"star_rating" TEXT,
"review_sum" TEXT,
"address" TEXT,
"mon_opening_hours" TEXT, "mon_last_order_time" TEXT,
"tue_opening_hours" TEXT, "tue_last_order_time" TEXT,
"wed_opening_hours" TEXT, "wed_last_order_time" TEXT,
"thu_opening_hours" TEXT, "thu_last_order_time" TEXT,
"fri_opening_hours" TEXT, "fri_last_order_time" TEXT,
"sat_opening_hours" TEXT, "sat_last_order_time" TEXT,
"sun_opening_hours" TEXT, "sun_last_order_time" TEXT,
"contact");

- db로 저장한 csv 데이터 id 있는 테이블에 복제

INSERT INTO restaurants(create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact)
SELECT create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact FROM hapjeong;
INSERT INTO restaurants(create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact)
SELECT create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact FROM hongdae;
INSERT INTO restaurants(create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact)
SELECT create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact FROM mangwon;
INSERT INTO restaurants(create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact)
SELECT create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact FROM sinchon;
INSERT INTO restaurants(create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact) 
SELECT create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact FROM yeonnamdong;
INSERT INTO restaurants(create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact) 
SELECT create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact FROM yeonhuidong;
INSERT INTO restaurants(create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact)
SELECT create_time, area, name, type, star_rating, review_sum, address, mon_opening_hours,mon_last_order_time,tue_opening_hours,tue_last_order_time,wed_opening_hours,wed_last_order_time,thu_opening_hours,thu_last_order_time,fri_opening_hours,fri_last_order_time,sat_opening_hours,sat_last_order_time,sun_opening_hours,sun_last_order_time, contact FROM yeoksamdong;


- db 나가기
.quit