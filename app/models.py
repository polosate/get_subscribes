from app import db
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text
from flask.ext.login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    login = Column(String(120), index = True, unique = True)
    password = Column(String(120), index = True, unique = True)
    ctn = Column(String(11), ForeignKey('ctns.ctn'), index = True, unique = True)
    # user_sessions = db.relationship('UserSession', backref = 'user', lazy = 'dynamic')

    def __repr__(self):
        return '<User {} {}>'.format(self.login, self.ctn)


class Ctn(db.Model):
    __tablename__ = 'ctns'
    ctn = Column(String(11), primary_key = True)

    
def get_user(user_id):
    return User.query.filter_by(id = user_id).first()

def is_phone_number_exists(ctn):
    return Ctn.query.filter_by(ctn=ctn).first()

def is_user_registrated(ctn):
    return User.query.filter_by(ctn=ctn).first()

def is_login_exists(login):
    return User.query.filter_by(login=login).first()