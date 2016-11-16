from flask import Flask, g
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin, current_user
from config import basedir

from social.apps.flask_app.routes import social_auth
from social.apps.flask_app.template_filters import backends
from social.apps.flask_app.default.models import init_social

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


BASE_DIR = '{}/../'.format(os.path.dirname(os.path.abspath(__file__)))


class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Anonymous'


template_folder= os.path.join(BASE_DIR, 'templates')
static_folder = os.path.join(BASE_DIR, 'static')


app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.config.from_object('config')
db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(Session)

app.register_blueprint(social_auth)
init_social(app, db_session)

lm = LoginManager()
lm.login_view = 'login'
lm.anonymous_user = Anonymous
lm.init_app(app)

from app import handlers, models
from .models import get_user


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


@app.before_request
def global_user():
    g.user = current_user._get_current_object()


@app.teardown_appcontext
def commit_on_success(error=None):
    if error is None:
        db_session.commit()
    else:
        db_session.rollback()
    db_session.remove()


@app.context_processor
def inject_user():
    try:
        return {'user': g.user}
    except AttributeError:
        return {'user': None}

app.context_processor(backends)
