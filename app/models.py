from app import db
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    email = Column(String(120), index = True, unique = True)
    nickname = Column(String(120), index = True, unique = True)
    ctn = Column(String(11), ForeignKey('ctns.ctn'), index = True, unique = True)
    # user_sessions = db.relationship('UserSession', backref = 'user', lazy = 'dynamic')

    def __repr__(self):
        return '<User {} {}>'.format(self.email, self.ctn)


class Ctn(db.Model):
    __tablename__ = 'ctns'
    ctn = Column(String(11), primary_key = True)

    