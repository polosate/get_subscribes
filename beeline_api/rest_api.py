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


# Убрать, ненужная функция, написана для тренировки
def get_personal_info(beeline_token, login):
    url = 'https://my.beeline.ru/api/1.0/sso/contactData?login=%s' % (login)
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
    try:
        response = response.json()
        if response.get('meta').get('code') == 20000:
            subscribes_list = response.get('subscriptions')
            if len(subscribes_list) == 0:
                result = "Подписок нет"
                return result, None
            else:
                result = subscribes_list
                return result, None
        else:
            result = response.get('meta').get('message')   
            return None, result         

    except Exception:
        return None, "Error_%s" % response.status_code



# https://my.beeline.ru/api/1.0/info/serviceAvailableList?ctn=9060447044
def get_available_subscriptions(): pass


if __name__ == '__main__':
    login = ''
    password = ''
    ctn = ''
    token = get_token(login, password)
    user_info = get_personal_info(token, login, ctn)
    print(user_info)
