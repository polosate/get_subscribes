from flask import Flask
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from config import basedir

BASE_DIR = '{}/../'.format(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
# print(basedir)

class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.login = 'Anonymous'


template_folder= os.path.join(BASE_DIR, 'templates')
static_folder = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.anonymous_user = Anonymous


from app import handlers, models
