from flask import Blueprint, Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from pagination import Pagination
from crawler.fileTransform import load_csv, naver_place_csv_to_db
from constant import dict_area_gu_to_dong, dict_searchtype_to_code, NULL
from crawler.Data_Crawl_and_Process import Data_Crawl_and_Process
from models import db, User, UserLike, Place, TypeCode
from secret import SECRET_KEY, KAKAO_JAVASCRIPT_KEY
import utils
from operator import itemgetter
from datetime import datetime

bp = Blueprint('cafe', __name__, url_prefix = '/cafe')