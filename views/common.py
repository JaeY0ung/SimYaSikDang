from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from crawler.fileTransform import naver_place_csv_to_db
from crawler.constant import dict_area_gu_to_dong, dict_searchtype_to_code
from crawler.Data_Crawl_and_Process import Data_Crawl_and_Process
from models import db, User, UserLike, Place, TypeCode
from datetime import datetime

bp = Blueprint('common', __name__, url_prefix = '/')

@bp.route('')
def index():
    return redirect(url_for('pub.index'))


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
        
    except Exception as e: #! 로그인한 유저가 없으면
        print('[디버깅] error:', e)
        return 'No User login', 403
        return redirect(url_for('auth.login'))
    
    
@bp.route('/singo')
@login_required
def singo():
    user    = User.query.filter_by(id = current_user.id).first()
    print(user.name)
    address = request.args.get('address', default='', type=str)
    name    = request.args.get('name',    default='', type=str)
    return render_template('singo.html', address = address, name = name, user = user)


@bp.route('/data-process')
def data_process():
    if not current_user.is_authenticated or current_user.username != "admin":
        return render_template('404.html')
    return render_template('data_process.html')
     

@bp.route('/crawl')
def crawl():
    if not current_user.is_authenticated or current_user.username != "admin":
        return render_template('404.html')
    data_processor = Data_Crawl_and_Process()
    data_processor.get_all_area()
    return redirect(url_for('common.data_process'))


@bp.route('/crawl-one')
def crawl_one():
    if not current_user.is_authenticated or current_user.username != "admin":
        return render_template('404.html')
    data_processor = Data_Crawl_and_Process()
    data_processor.get_one('경포동', '술집')
    return redirect(url_for('common.data_process'))


@bp.route('/crawl-pub')
def crawl_pub():
    if not current_user.is_authenticated or current_user.username != "admin":
        return render_template('404.html')   
    data_processor = Data_Crawl_and_Process()
    data_processor.get_pub_only()
    return redirect(url_for('common.data_process'))


@bp.route('/crawl-restaurant')
def crawl_restaurant():
    if not current_user.is_authenticated or current_user.username != "admin":
        return render_template('404.html')
    data_processor = Data_Crawl_and_Process()
    data_processor.get_restaurant_only()
    return redirect(url_for('common.data_process'))
 

@bp.route('/save-data-to-db')
def save_data_to_db():
    if not current_user.is_authenticated or current_user.username != "admin":
        return render_template('404.html')
    
    for dongs in dict_area_gu_to_dong.values():
        for dong in dongs:
            for searchtype, code in dict_searchtype_to_code.items():
                try:
                    naver_place_csv_to_db(dong, code)
                except:
                    print(f'{dong} {searchtype} 데이터 저장 실패')
    return redirect(url_for('common.data_process'))

    
@bp.route('/make-typecode')
def make_typecode():
    #! (일회용) TypeCode 테이블에 정보 넣기
    pub        = TypeCode.query.filter_by(type="술집").first()
    cafe       = TypeCode.query.filter_by(type="카페").first()
    restaurant = TypeCode.query.filter_by(type="식당").first()
    if not pub:
        pub_typecode = TypeCode(type="술집", code="A")
        db.session.add(pub_typecode)
        print('술집 코드 생성')
    if not cafe:
        cafe_typecode = TypeCode(type="카페", code="B")
        db.session.add(cafe_typecode)
        print('카페 코드 생성')
    if not restaurant:
        restaurant_typecode = TypeCode(type="식당", code="C")
        db.session.add(restaurant_typecode)
        print('식당 코드 생성')
    db.session.commit()
    return redirect(url_for('common.data_process'))


@bp.route('/make-admin')
def make_admin():
    isAdminExist = User.query.filter_by(username = 'admin').first()
    if not isAdminExist:
        from werkzeug.security import generate_password_hash
        admin = User(username      = 'admin', 
                     password_hash = generate_password_hash('admin'), 
                     nickname      = 'ADMIN', 
                     contact       = '01012345678',
                     email         = 'j0@naver.com',
                     name          = '관리자')
        db.session.add(admin)
        db.session.commit()
        print('admin 회원가입 완료')
    print('admin 회원가입 실패')
    return redirect(url_for('common.index'))

@bp.route('/remove-admin')
def remove_admin():
    isAdminExist = User.query.filter_by(username = 'admin').first()
    if isAdminExist:
        User.query.filter_by(username = 'admin').delete()
        db.session.commit()
        print('admin 회원탈퇴 완료')
    print('admin 회원탈퇴 실패')
    return redirect(url_for('common.index'))