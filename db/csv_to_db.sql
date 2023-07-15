- 모든 테이블 삭제
DROP TABLE mangwon;

-csv 파일 db로 저장

.mode csv
.import ../csv/망원_processed.csv mangwon2

- id를 가진 table2 생성

CREATE TABLE IF NOT EXISTS mangwon(
"UUID" INTEGER PRIMARY KEY AUTOINCREMENT,
"name" TEXT,
"type" TEXT,
"star_rating" TEXT,
"review_sum" TEXT,
"address" TEXT,
"월opening_hours" TEXT, "월last_order_time" TEXT,
"화opening_hours" TEXT, "화last_order_time" TEXT,
"수opening_hours" TEXT, "수last_order_time" TEXT,
"목opening_hours" TEXT, "목last_order_time" TEXT,
"금opening_hours" TEXT, "금last_order_time" TEXT,
"토opening_hours" TEXT, "토last_order_time" TEXT,
"일opening_hours" TEXT, "일last_order_time" TEXT,
"contact");

- db로 저장한 csv 데이터 id 있는 테이블에 복제

INSERT INTO mangwon(name,type,star_rating,review_sum,address,월opening_hours,월last_order_time,화opening_hours,화last_order_time,수opening_hours,수last_order_time,목opening_hours,목last_order_time,금opening_hours,금last_order_time,토opening_hours,토last_order_time,일opening_hours,일last_order_time,contact) 
SELECT name,type,star_rating,review_sum,address,월opening_hours,월last_order_time,화opening_hours,화last_order_time,수opening_hours,수last_order_time,목opening_hours,목last_order_time,금opening_hours,금last_order_time,토opening_hours,토last_order_time,일opening_hours,일last_order_time,contact FROM mangwon2;

- csv로 만든 기존 테이블 삭제

DROP TABLE mangwon2;

- db 나가기
.quit