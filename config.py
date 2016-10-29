import os


CSRF_ENABLED = True
SECRET_KEY = 'my-first-python-project-secret-key'

basedir = os.path.abspath(os.path.dirname(__file__))

login = 'postgres'
password = 'postgres'
host = 'localhost'
port = 5432
schema = 'mydb_1'    

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(login, password, host, port, schema)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True