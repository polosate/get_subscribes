from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(120), index=True, unique=True)
    password = Column(String(120), index=True, unique=True)
    ctn = Column(String(11), ForeignKey('ctns.ctn'), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    birth_day = Column(Date, nullable=True)
    about_me = Column(Text, nullable=True)

    def __repr__(self):
        return '<User {} {}>'.format(self.username, self.ctn)


class Ctn(db.Model):
    __tablename__ = 'ctns'
    ctn = Column(String(11), primary_key=True)


class Tasks(db.Model):
    __tablename__ = 'check_subscriptions'
    task_id = Column(String, primary_key=True, index=True)
    subscription_id = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)

def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

def is_phone_number_exists(ctn):
    return Ctn.query.filter_by(ctn=ctn).first()

def is_user_registrated(ctn):
    return User.query.filter_by(ctn=ctn).first()

def is_login_exists(username):
    return User.query.filter_by(username=username).first()
