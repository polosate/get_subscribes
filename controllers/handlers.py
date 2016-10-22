from flask import Flask, abort, request, redirect, url_for, make_response, render_template
from beeline_api.rest_api import get_beeline_token, get_personal_info, get_subscribes
from auth.session import Session, set_token, check_token, set_session, get_session
from .app import app

# app = Flask(__name__)


# перенести все рендеры в отдельные темлэйты
def render_login_form(args):
    return render_template('login.html', error=args.get('error'))

# перенести все рендеры в отдельные темлэйты
def render_dashboard_page(user_info, subscriptions_list=None, subscriptions_str = None, errors=None):
    return render_template('dashboard.html', user_info=user_info, subscriptions_list=subscriptions_list, \
        subscriptions_str = subscriptions_str,errors=errors)
    # try:
    #     template = """
    #         <h2>Добро пожаловать, %(firstName)s %(lastName)s!</h2>
    #         <p><b>Ваш адрес:</b> <i>%(invoiceAddr)s</i></p>
    #     """
    #     body = template % user_info
    #     body += """
    #         <p>Ваши подписки:</p>
    #         <p>%s</p>
    #     """ % subscriptions
    # except (KeyError, ValueError):
    #     template = """
    #         <h2>%S</h2>
    #     """ % user_info
    #     body = template

    # return body


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        body = render_login_form(request.args)
        response = make_response(body)
        set_token(response)
        return response
    else:
        token = request.cookies.get('token')
        if not check_token(token):
            return redirect(url_for('login', error='Включите куки!'))

        # получаем параметры из пришедшего поста (в дальнейшес это будет только ctn)
        ctn = request.form.get('ctn')
        login = request.form.get('login')
        password = request.form.get('password')

        """
        Тут нужна проверка, что ctn в нашей базе. Если нет, то снова редирект на / с ошибкой "Такой номер у нас не заргеан"
        Если номер у нас есть, автоматом подставляем наши логин и пароль от апи билайна. Вводить с формы их не надо.
        """

        # получаем токен или ошибку (пример токена 51BF96B928C8C71124BE61C1BF787B23)
        beeline_token, error_message = get_beeline_token(login, password)

        if not beeline_token:
            return redirect(url_for('login', error=error_message))
        else:
            session = Session(beeline_token, login, ctn)
            set_session(session, token)
            return redirect(url_for('dashboard'))


@app.route("/dashboard")
def dashboard(): 
        token = request.cookies.get('token')
        session = get_session(token)
        if not session:
            return redirect(url_for('login', error="Аутентифицируйтесь, блеа!"))

        beeline_token = session.beeline_token
        ctn = session.ctn
        login = session.login

        user_info, error_message = get_personal_info(beeline_token, login)

        if not user_info:
            user_info = error_message

        subscriptions, errors = get_subscribes(beeline_token, ctn)

        if not errors:
            if isinstance(subscriptions, list):
                response = render_dashboard_page(user_info, subscriptions_list = subscriptions)
            else:
                response = render_dashboard_page(user_info, subscriptions_str=subscriptions)
        else:
            response = render_dashboard_page(user_info, errors=errors)

        return response
