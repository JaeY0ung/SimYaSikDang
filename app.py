from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from pagination import Pagination
from crawler.fileTransform import load_csv, naver_place_csv_to_db
from crawler.constant import dict_area_gu_to_dong, dict_searchtype_to_code, SECRET_KEY, NULL
from crawler.Data_Crawl_and_Process import Data_Crawl_and_Process
from models import db, User, UserLike, Place, TypeCode
from secret import KAKAO_JAVASCRIPT_KEY
from datetime import datetime
from operator import itemgetter
from datetime import datetime
from views import common, pub, auth, cafe

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


# Migrate 설정
migrate = Migrate(app, db)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8000) # host="0.0.0.0"