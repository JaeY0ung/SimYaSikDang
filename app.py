from flask import Flask, render_template, request, redirect, url_for
# from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
# from pagination import Pagination
# from crawler.fileTransform import load_csv, naver_place_csv_to_db
from constant import dict_area_gu_to_dong, dict_searchtype_to_code, NULL
from secret import SECRET_KEY
# from crawler.Data_Crawl_and_Process import Data_Crawl_and_Process
from models import db, User, UserLike, Place, TypeCode
from secret import KAKAO_JAVASCRIPT_KEY, GMAIL_PASSWORD, GMAIL_ID
# from datetime import datetime
# from operator import itemgetter
# from datetime import datetime
from views import common, pub, auth, cafe
from flask_mail import Mail, Message
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simyasikdang.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
app.register_blueprint(common.bp)
app.register_blueprint(pub.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(cafe.bp)

auth.login_manager.init_app(app)
db.init_app(app)

app.config['MAIL_SERVER']   = 'smtp.gmail.com'
app.config['MAIL_PORT']     = 465
app.config['MAIL_USERNAME'] = GMAIL_ID
app.config['MAIL_PASSWORD'] = GMAIL_PASSWORD
app.config['MAIL_USER_TLS'] = False
app.config['MAIL_USE_SSL']  = True
mail = Mail(app)

@app.route('/email', methods = ["GET", "POST"])
def email():
    if request.method == "POST":
        find_type  = request.form['type']
        find_email = request.form['email']
        msg = Message('심야식당', sender = 'simyasikdang2023@gmail.com', recipients = [find_email])

        content = {}
        if find_type == 'username':
            find_name = request.form['name']
            user = User.query.filter_by(name = find_name, email = find_email).first()
        elif find_type == 'password':
            find_username  = request.form['username']
            user = User.query.filter_by(username = find_username, email = find_email).first()
            if user:
                new_password = str(uuid.uuid4())[0:8]
                user.set_password(new_password)
                db.session.commit()
                content['new_password'] = new_password

        if user:
            msg.html = render_template('send_email.html', find_type = find_type, user = user, content = content)
            mail.send(msg)
            print('전송 완료')
            return redirect(url_for('auth.login'))
        else:
            print('[디버깅] 전송 실패')
            return redirect(url_for('auth.user_info'))

# Migrate 설정
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8000) # host="0.0.0.0"