import requests

def get_beeline_token(login, password):
    """
    По логину и паролю по api beeline получаем токен билайна
    """ 
    url = 'https://my.beeline.ru/api/1.0/auth?login=%s&password=%s' % (login, password)
    
    res = requests.get(url)

    try:
        res = res.json()
        if res['meta']['code'] == 20000:
            beeline_token = res['token']
            return beeline_token, ""
        else:
            return None, res['meta']['message']
    except Exception:
        return None, "Error_%s" % res.status_code


def get_personal_info(beeline_token, login, ctn):
    url = 'https://my.beeline.ru/api/1.0/sso/contactData?login=%s&ctn=%s' % (login, ctn)
    cookies = {'token': beeline_token}
    contact_data = requests.get(url, cookies=cookies)
    try:
        return contact_data.json(), None
    except Exception:
        return None, "user_info json error" 


def get_subscribes(beeline_token, ctn):
    is_stub = False
    if is_stub:
        url = 'http://127.0.0.1:5050/'
    else:
        url = 'https://my.beeline.ru/api/1.0/info/subscriptions?ctn=%s' % ctn
        
    cookies = {'token': beeline_token}
    response = requests.get(url, cookies=cookies)
    subscribes_list = response.json().get('subscriptions')

    if len(subscribes_list) == 0:
        return "Подписок нет"
    else:
        return subscribes_list


if __name__ == '__main__':
    login = ''
    password = ''
    ctn = ''
    token = get_token(login, password)
    user_info = get_personal_info(token, login, ctn)
    print(user_info)
