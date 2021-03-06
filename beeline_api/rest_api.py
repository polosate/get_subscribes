import requests


LOGIN = ''
PASSWORD = ''
is_stub = True



def get_beeline_token():
    """
    По логину и паролю по api beeline получаем токен билайна
    пример токена 51BF96B928C8C71124BE61C1BF787B23
    """
    url = '=%s' % (LOGIN, PASSWORD)
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


def get_subscriptions(ctn):
    bt, _ = get_beeline_token()
    if is_stub:
        url = 'http://127.0.0.1:5050/get'
    else:
        url = '=%s' % ctn

    cookies = {'token': bt}
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


def remove_subscriptions(ctn, subscription_id):
    bt, _ = get_beeline_token()
    if is_stub:
        url = 'http://127.0.0.1:5050/remove?subscriptionId=%s' % subscription_id
    else:
        url = '={}&subscriptionId={}'.format(ctn, subscription_id)

    cookies = {'token': bt}
    response = requests.get(url, cookies=cookies)

    response = response.json()

    if response.get('meta').get('code') == 20000:
        result = 'Скоро отключим, обновите страницу'
    else:
        result = response.get('meta').get('message')

    return result


if __name__ == '__main__':
    login = ''
    password = ''
    ctn = ''
    token = get_token(login, password)
    user_info = get_personal_info(token, login, ctn)
    print(user_info)
