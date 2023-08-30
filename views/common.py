from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from crawler.fileTransform import naver_place_csv_to_db
from crawler.constant import dict_area_gu_to_dong, dict_searchtype_to_code
from crawler.Data_Crawl_and_Process import Data_Crawl_and_Process
from models import db, User, UserLike, Place
from datetime import datetime

bp = Blueprint('common', __name__, url_prefix = '/')

@bp.route('')
def index():
    return redirect(url_for('pub.index'))


@bp.route('/singo')
@login_required
def singo():
    user    = User.query.filter_by(id = current_user.id).first()
    print(user.name)
    address = request.args.get('address', default='', type=str)
    name    = request.args.get('name',    default='', type=str)
    return render_template('singo.html', address = address, name = name, user = user)


@bp.route('/place/<place_uuid>/like' , methods=["GET", "POST", "DELETE"])
def place_like(place_uuid):
    try: #! 로그인한 유저가 있으면
        if request.method == "POST":
            place = Place.query.filter_by(uuid = place_uuid).first()
            
            user_like_obj_exist = UserLike.query.filter_by(userid = current_user.id,
                                                    placeid = place.id).first()
            if not user_like_obj_exist:
                user_like_obj = UserLike(userid = current_user.id,
                                        placeid = place.id,
                                        likedate = datetime.now())
                db.session.add(user_like_obj)
                db.session.commit()
                return 'Resource posted successfully', 204
            else:
                return 'Resource not posted (already exist)', 404


        elif request.method == "DELETE":
            place = Place.query.filter_by(uuid = place_uuid).first()
            user_like_obj_exist = UserLike.query.filter_by(userid = current_user.id,
                                    placeid = place.id).delete()
            if user_like_obj_exist:
                db.session.commit()
                # TODO : redirect(url_for('pub.index')) 안 써도 되는지?
                return 'Resource deleted successfully', 204
            else:
                return 'Resource not found', 404
            
        return 'Nothing TO DO', 404
        
    except AttributeError: #! 로그인한 유저가 없으면
        return 'No User login', 404
        return redirect(url_for('auth.login'))
    


@bp.route('/data-process')
@login_required
def data_process():
    if current_user.username == "admin":
        return render_template('data_process.html')
    return render_template('404.html')


@bp.route('/crawl')
@login_required
def crawl():
    if current_user.username == "admin":
        data_processor = Data_Crawl_and_Process()
        data_processor.get_all_area()
        return redirect(url_for('common.data_process'))
    return render_template('404.html')

@bp.route('/crawl-pub')
@login_required
def crawl_pub():
    if current_user.username == "admin":
        data_processor = Data_Crawl_and_Process()
        data_processor.get_pub_only()
        return redirect(url_for('common.data_process'))
    return render_template('404.html')


@bp.route('/save-data-to-db')
@login_required
def save_data_to_db():
    if current_user.username == "admin":
        #! db에 저장 코드
        for dongs in dict_area_gu_to_dong.values():
            for dong in dongs:
                for searchtype, code in dict_searchtype_to_code.items():
                    try:
                        naver_place_csv_to_db(dong, code)
                    except:
                        print(f'{dong} {searchtype} 데이터 저장 실패')
        return redirect(url_for('common.data_process'))
    return render_template('404.html')


@bp.route('/make-admin')
def make_admin():
    #! (일회용) 관리자 계정 자동 생성 코드
    isAdminExist = User.query.filter_by(username = 'admin').first()
    if not isAdminExist:
        from werkzeug.security import generate_password_hash
        admin = User(username = 'admin', 
                     password_hash = generate_password_hash('admin'), 
                     nickname = 'ADMIN', 
                     contact = '010-1234-5678',
                     email = 'j0@naver.com',
                     name  = '관리자')
        db.session.add(admin)
        db.session.commit()
        print('admin 회원가입 완료')
    print('admin 회원가입 실패')
    return redirect(url_for('common.index'))

@bp.route('/remove-admin')
def remove_admin():
    #! (일회용) 관리자 계정 자동 생성 코드
    isAdminExist = User.query.filter_by(username = 'admin').first()
    if isAdminExist:
        User.query.filter_by(username = 'admin').delete()
        db.session.commit()
        print('admin 회원탈퇴 완료')
    print('admin 회원탈퇴 실패')
    return redirect(url_for('common.index'))