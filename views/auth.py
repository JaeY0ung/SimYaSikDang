from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix = '/')


def yoil(): #! 오늘이 무슨 요일인지 구하는 함수 return (한글 요일, 영어 요일)
    today = datetime.today().weekday()
    hour_now = datetime.now().hour
    yoil_arr_kor = ['월','화','수','목','금','토','일']
    yoil_arr_eng = ['mon','tue','wed','thu','fri','sat','sun']
    if hour_now <= 10: #! 술집이므로 오전 10:59까지는 전날 시간으로 계산하는 것이 맞다고 생각!
        return yoil_arr_kor[today], yoil_arr_eng[today-1]
    return yoil_arr_kor[today], yoil_arr_eng[today]

login_manager = LoginManager()  #! 로그인 매니저 생성
login_manager.login_view = "auth.login" #! 로그인 페이지 URI 명시
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST": #! (회원가입)
        username       = request.form["username"]
        password       = request.form["password"]
        password_again = request.form["password_again"]
        name           = request.form["name"]
        nickname       = request.form["nickname"]
        contact        = request.form["contact"].replace('-', '')
        email          = request.form["email"]

        if password != password_again:
            print(f'비밀번호를 다시 입력해주세요')
            return redirect(url_for('auth.register'))

        email = request.form["email"]

        existing_user_by_userid = User.query.filter_by(username = username).first()
        existing_user_by_email  = User.query.filter_by(email = email).first()

        if existing_user_by_userid:
            print('이미 있는 아이디입니다.')
            return redirect(url_for('auth.register'))
        
        elif existing_user_by_email:
            print('이미 사용하는 이메일입니다.')
            return redirect(url_for('auth.register'))

        new_user = User(username = username, 
                        name     = name,
                        nickname = nickname,
                        contact  = contact,
                        email    = email)
        
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('common.index'))
    return render_template('register.html', today_yoil_kor = yoil()[0])

@bp.route('/users', methods=['GET'])
def users():
    if request.method == 'GET': #! (회원 가입시) 아이디, 이메일 중복 체크
        input_username = request.args.get('username', default='', type=str)
        input_email    = request.args.get('email',    default='', type=str)

        user = ''
        if input_username:
            user = User.query.filter_by(username = input_username).first()

        if input_email:
            user = User.query.filter_by(email    = input_email   ).first()

        if user == None:
            exist = 'false'
        else:
            exist = 'true'

        return jsonify({'exist' : exist})
    

@bp.route('/user-info', methods=["GET", "PUT"]) #! 나의 정보 확인/수정 창
def user_info():
    if request.method == "PUT": #! (회원정보 수정 시 / 로그인 필요) @login_required
        return 'Modify User Info Successfully', 204
    
    elif request.method == "GET": #! (아이디/비밀번호 찾기 링크 클릭 시)
        return render_template('user_info_find.html', current_user = current_user, today_yoil_kor = yoil()[0])
    
    return render_template('user_info.html', current_user = current_user, today_yoil_kor = yoil()[0])


@bp.route('/withdraw', methods = ["GET", "DELETE"])
@login_required
def withdraw():
    if request.method == "DELETE": #! (회원 탈퇴 시 / 로그인 필요)
        return 'Delete User Successfully', 204 # return redirect(url_for('common.index'))
    return render_template('withdraw.html', today_yoil_kor = yoil()[0])


@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username = username).first()
        if user and user.check_password(password):
            login_user(user) # 유저 로그인
            print(f'{current_user.username} : 로그인에 성공했습니다.')
            return redirect(url_for('common.index'))
        else:
            print(f'로그인에 실패횄습니다.')
            return redirect(url_for('auth.login'))
        
    #? 3. 성공시 로그인 정보 저장하고 로그인 페이지로 이동
    #?    실패시 오류 알려주기
    return render_template('login.html', today_yoil_kor = yoil()[0])


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('common.index'))

