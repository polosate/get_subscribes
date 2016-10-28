import random, string
from db.models_1 import db_session, Session, User
from beeline_api.rest_api import get_beeline_token
from flask import redirect, url_for

ADMIN_LOGIN = 'Westek'
ADMIN_PWD = 'DSsdg3qfdJ'

COOKIE_LENGTH = 20
STRING_LOWERCASE = "qwertyuiopasdfghjklzxcvbnm"


def generate_random_token():
   return ''.join(random.choice(STRING_LOWERCASE) for i in range(COOKIE_LENGTH))


def set_token(response):    
    token = generate_random_token()
    response.set_cookie('token', token)
    session = Session(token)
    db_session.add(session)
    db_session.commit()


def check_token(token):
    is_token_exists = db_session.query(Session).filter(Session.token==token).first()
    return is_token_exists    

def get_session_from_db(token):
    our_session = db_session.query(Session).filter(Session.token==token).first()
    return our_session


def get_user(ctn):
    return db_session.query(User).filter(User.ctn == ctn).first()


def get_session(token): 
    if check_token(token):
        session = db_session.query(Session).filter(Session.token==token).first()
    else:
        return None        
    if not session.user_id:
        return None
    else:
        return session


def set_session(beeline_token, token, ctn):
    user_id = get_user(ctn).id
    session = get_session_from_db(token)
    session.user_id = user_id
    session.beeline_token = beeline_token
    db_session.commit()


def authorization(request, fail_redirect, success_redirect):
        our_ctn = request.form.get('ctn')
        our_login = request.form.get('login')
        our_password = request.form.get('password')
        token = request.cookies.get('token')

        if not check_token(token):
            return redirect(url_for(fail_redirect, error='Включите куки!'))

        if not get_user(our_ctn):
            return redirect(url_for(fail_redirect, error="Не зарегистрирован"))            
        else:
            login = db_session.query(User).filter(User.ctn==our_ctn).first().login
            password = db_session.query(User).filter(User.ctn==our_ctn).first().passwd

            if our_login == login and our_password == password:
                beeline_token, error_message = get_beeline_token(ADMIN_LOGIN, ADMIN_PWD)
                if not beeline_token:
                    return redirect(url_for(fail_redirecth, error=error_message))
                else:
                    set_session(beeline_token, token, our_ctn)
                    return redirect(url_for(success_redirect))                    
            else:
                return redirect(url_for(fail_redirect, error="Не верный логин и/или пароль"))
