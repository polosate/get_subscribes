import os


CSRF_ENABLED = True
SECRET_KEY = 'my-first-python-project-secret-key'

SESSION_COOKIE_NAME = 'psa_session'
DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))

LOGIN = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = 5432
SCHEMA = 'mydb_1'    

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(LOGIN, PASSWORD, HOST, PORT, SCHEMA)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG_TB_INTERCEPT_REDIRECTS = False
SESSION_PROTECTION = 'strong'

SOCIAL_AUTH_LOGIN_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/askphone'
SOCIAL_AUTH_USER_MODEL = 'app.models.User'
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['keep']
SOCIAL_AUTH_REMEMBER_SESSION_NAME = 'remember_me'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '445988658675-sff7qtvhl2esl6rhhk47a321f2ccmqsj.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'Nf_cnbzz0i37PogRdp6cmrFA'
SOCIAL_AUTH_GITHUB_KEY = 'eba194d2ec1ee182a145'
SOCIAL_AUTH_GITHUB_SECRET = '84954f2060793cfe37e028726a097c6ea4b49585'

SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social.backends.github.GithubOAuth2',
 )
