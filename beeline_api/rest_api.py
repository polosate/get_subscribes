import requests

def get_beeline_token(login, password):
    """
    По логину и паролю по api beeline получаем токен
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
    return contact_data.json()


def get_subscribes(beeline_token, ctn):
    url = 'https://my.beeline.ru/api/1.0/info/subscriptions?%s' % ctn
    cookies = {'token': beeline_token}
    contact_data = requests.get(url, cookies=cookies)
    subscribes_list = requests.get(url)
    return subscribes_list


if __name__ == '__main__':
    login = ''
    password = ''
    ctn = ''
    token = get_token(login, password)
    user_info = get_personal_info(token, login, ctn)
    print(user_info)
