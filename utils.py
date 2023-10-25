from datetime import datetime

def yoil(): #! 오늘이 무슨 요일인지 구하는 함수 return (한글 요일, 영어 요일)
    today = datetime.today().weekday()
    hour_now = datetime.now().hour
    yoil_arr_kor = ['월','화','수','목','금','토','일']
    yoil_arr_eng = ['mon','tue','wed','thu','fri','sat','sun']
    if hour_now <= 10: #! 술집이므로 오전 10:59까지는 전날 시간으로 계산하는 것이 맞다고 생각!
        return yoil_arr_kor[today], yoil_arr_eng[today-1]
    return yoil_arr_kor[today], yoil_arr_eng[today]

def time(): #! 지금이 몇신지 구하는 함수 return (시간, 분)
    now = datetime.now()
    return now.hour, now.minute