import random, string
from db.db_methods import db_session, Session
import pickle

COOKIE_LENGTH = 20
STRING_LOWERCASE = "qwertyuiopasdfghjklzxcvbnm"

sessions = {}



def generate_random_token():
   return ''.join(random.choice(STRING_LOWERCASE) for i in range(COOKIE_LENGTH))


def set_token(response):    
    token = generate_random_token()
    response.set_cookie('token', token)
    session = Session(token)
    db_session.add(session)
    db_session.commit()

def check_token(token):
    session = Session
    is_token_exists = db_session.query(session).filter(Session.token==token).exists()
    return is_token_exists


def get_session(response):
    token = request.cookies.get('token')
    if check_token(token):


    return sessions.get(token)


def set_session(session, token):
    sessions[token] = session


class Session():
    def __init__(self, beeline_token, login, ctn):
        self.beeline_token = beeline_token
        self.login = login
        self.ctn = ctn
