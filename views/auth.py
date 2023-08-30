from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User

bp = Blueprint('auth', __name__, url_prefix = '/auth')

login_manager = LoginManager()  #! 로그인 매니저 생성
login_manager.login_view = "auth.login" #! 로그인 페이지 URI 명시
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        userid = request.form["id"]
        pw = request.form["pw"]
        pw_again = request.form["pw_again"]

        if pw != pw_again:
            print(f'비밀번호를 다시 입력해주세요')
            return redirect(url_for('auth.register'))

        email = request.form["email"]

        existing_user_by_userid = User.query.filter_by(userid=userid).first()
        existing_user_by_email  = User.query.filter_by(email=email).first()
        if existing_user_by_userid:
            print('이미 있는 아이디입니다.')
            return redirect(url_for('auth.register'))
        
        elif existing_user_by_email:
            print('이미 사용하는 이메일입니다.')
            return redirect(url_for('auth.register'))

        new_user = User(userid = userid, email = email)
        new_user.set_password(pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('common.index'))
    return render_template('register.html')


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
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('common.index'))