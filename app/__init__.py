from flask import Flask
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir

BASE_DIR = '{}/../'.format(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
# print(basedir)


template_folder= os.path.join(BASE_DIR, 'templates')
app = Flask(__name__, template_folder=template_folder)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import handlers, models
