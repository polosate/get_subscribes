import random, string

COOKIE_LENGTH = 20
STRING_LOWERCASE = "qwertyuiopasdfghjklzxcvbnm"

sessions = {}


def generate_random_token():
   return ''.join(random.choice(STRING_LOWERCASE) for i in range(COOKIE_LENGTH))


def set_token(response):
    token = generate_random_token()
    response.set_cookie('token', token)
    sessions[token] = None


def check_token(token):
    if token in sessions:
        return True
    else:
        return False


def get_session(): pass


def set_session(session, token):
    sessions[token] = session


class Session():
    def __init__(self, beeline_token, login, ctn):
        self.beeline_token = beeline_token
        self.login = login
        self.cnt = ctn
