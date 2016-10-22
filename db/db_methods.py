from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text

login = 'postgres'
password = 'postgres'
host = 'localhost'
port = 5432
schema = 'get_subscriptions'


url = 'postgresql://{}:{}@{}:{}/{}'.format(login, password, host, port, schema)
engine = create_engine(url)

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(120), unique = True)
    ctn = Column(String(11), unique = True)
    login = Column(String(50))
    passwd = Column(String(50))

    def __init__(self, first_name = None, last_name = None, email = None, ctn = None, login = None, passwd = None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.ctn = ctn
        self.login = login
        self.passwd = passwd

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)

class Session(Base):
    __tablename__ = 'sessions'
    token = Column(String(20), primary_key = True)
    session = Column(Text)
    user_id = -1

    def __init__(self, token = None, session = None):
        self.token = token
        self.session = session

    def load(self):
        sess = self.query.filter('token' == self.token).first()

    # def check_token(self, token):
    #     pass

    # def get_session():
    #     pass

    # def set_session():
    #     pass
