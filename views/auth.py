from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix = '/auth')


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
    return User.query.filter_by(id = user_id).first()


@bp.route('/register', methods = ["GET", "POST"]) # 회원가입 창에서 폼 성공적으로 제출 시
def register():
    if request.method == "POST": #! (회원가입)
        username       = request.form["username"]
        password       = request.form["password"]
        password_again = request.form["password-again"]
        name           = request.form["name"]
        nickname       = request.form["nickname"]
        contact        = request.form["contact"].replace('-', '')
        email          = request.form["email"]

        # 한 번 더 체크 (없어도 무방한가?)
        if password != password_again: 
            print(f'비밀번호를 다시 입력해주세요')
            return redirect(url_for('auth.register'))
        exist_user_by_userid = User.query.filter_by(username = username).first()
        if exist_user_by_userid:
            print('이미 있는 아이디입니다.')
            return redirect(url_for('auth.register'))
        exist_user_by_email  = User.query.filter_by(email = email).first()
        if exist_user_by_email:
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
        return redirect(url_for('common.index'), current_user = current_user)
    return render_template('register.html', today_yoil_kor = yoil()[0])

@bp.route('/edit', methods=["PUT"])
def edit():
    if request.method == "PUT":
        data = request.get_json()
        print(f'[디버깅] data: {data}')
        name          = data.get("name", "")
        username      = data.get("username", "")
        nickname      = data.get("nickname", "")
        contact       = data.get("contact", '').replace('-', '')
        email         = data.get("email", "")
        password      = data.get("password", "")
        password_new  = data.get("passwordNew", "")

        user = User.query.filter_by(name = name,
                                    username = username).first() 
        if user.check_password(password):
            user.nickname = nickname
            user.contact = contact
            user.email = email
            user.set_password(password_new)
            db.session.commit()
        return redirect(url_for('common.index'))
    return redirect(url_for('auth.user_info'))

@bp.route('/check', methods=['GET', 'POST', 'PUT']) # 회원 가입 창, 회원정보 수정창
def users():
    if request.method == 'GET': # 회원가입 시 아이디, 닉네임, 이메일 중복 체크
        input_username = request.args.get('username', default='', type=str)
        input_nickname = request.args.get('nickname', default='', type=str)
        input_email    = request.args.get('email',    default='', type=str)

        if input_username:
            user = User.query.filter_by(username = input_username).first()
        elif input_nickname:
            user = User.query.filter_by(nickname = input_nickname).first()
        elif input_email:
            user = User.query.filter_by(email = input_email).first()
        else:
            user = ''

        if user == None or user == '' or user == False:
            exist = 'false'
        else:
            exist = 'true'

        return jsonify({'exist' : exist})
    
    elif request.method == 'PUT': # 정보 수정에서 email, nickname
        input_username = request.get_json().get('username', '')
        input_email    = request.get_json().get('email', '')
        input_nickname = request.get_json().get('nickname', '')

        if input_username and input_email:
            user_check_only_email = User.query.filter_by(email = input_email).first()
            if not user_check_only_email or user_check_only_email.username == input_username:
                user = None # user 본인의 이메일인 경우 이메일을 쓰는 계정이 없다고 가정
            else: # 이메일을 자신이 아닌 다른 사용자가 사용한다면
                user = user_check_only_email
        elif input_username and input_nickname:
            user_check_only_nickname = User.query.filter_by(nickname = input_nickname).first()
            if not user_check_only_nickname or user_check_only_nickname.username == input_username:
                user = None # user 본인의 닉네임인 경우 닉네임을 쓰는 계정이 없다고 가정
            else: # 닉네임을 자신이 아닌 다른 사용자가 사용한다면
                user = user_check_only_nickname
        else:
            user = ''

        if user == None or user == '' or user == False:
            exist = 'false'
        else:
            exist = 'true'

        return jsonify({'exist' : exist})
    
    elif request.method == 'POST': # 회원정보 수정에서 유저의 비밀번호가 맞는지 확인 username, password로 확인
        input_username = request.get_json().get('username', '')
        input_password = request.get_json().get('password', '')
        if input_username and input_password:
            user_check_only_username = User.query.filter_by(username = input_username).first()
            if user_check_only_username.check_password(input_password): # 아이디, 비번이 모두 맞을 때
                user = user_check_only_username
            else: # 비밀번호가 틀릴 때
                user = None
        else:
            user = ''

        if user == None or user == '' or user == False:
            exist = 'false'
        else:
            exist = 'true'
        return jsonify({'exist' : exist})
    

@bp.route('/user-info', methods=["GET", "PUT"]) # 나의 정보 확인, 수정 페이지
def user_info():
    if request.method == "PUT": # (회원정보 수정 시/ 로그인 필요) @login_required
        return 'Modify User Info Successfully', 204
    return render_template('user_info.html', current_user = current_user, today_yoil_kor = yoil()[0])

@bp.route('/user-info/<find_type>') # 아이디/비말번호 찾기
def find_info(find_type):
    if find_type == 'username':
        return render_template('user_info_find_username.html', current_user = current_user, today_yoil_kor = yoil()[0])
    elif find_type == 'password':
        return render_template('user_info_find_password.html', current_user = current_user, today_yoil_kor = yoil()[0])
    return render_template('404.html')


@bp.route('/withdraw', methods = ["GET", "DELETE"])
@login_required
def withdraw():
    if request.method == "DELETE": #! (회원 탈퇴 시 / 로그인 필요)
        user_id = request.get_json().get('userId', '')
        print(user_id)
        User.query.filter_by(id = user_id).delete()
        db.session.commit()
        return 'Delete User Successfully', 204
    return render_template('withdraw.html', today_yoil_kor = yoil()[0])


@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username = username).first()
        if user and user.check_password(password):
            login_user(user) # 유저 로그인
            print(f'[login] {current_user.username}: 로그인 성공')
            return redirect(url_for('common.index'))
        else:
            print(f'로그인에 실패횄습니다.')
            return redirect(url_for('auth.login'))
    return render_template('login.html', today_yoil_kor = yoil()[0])


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('common.index'))

@bp.route('/users-info', methods=["GET", "PUT", "DELETE"]) #! 나의 정보 확인/수정 창
def users_info():
    if not current_user.is_authenticated or current_user.username != "admin":
        return redirect(url_for('common.index'))
    users = User.query.all()
    return render_template('users_info.html', users = users, today_yoil_kor = yoil()[0])