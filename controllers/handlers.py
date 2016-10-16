from flask import Flask, abort, request, redirect, url_for, make_response
from beeline_api.rest_api import get_beeline_token, get_personal_info, get_subscribes
from auth.session import Session, set_token, check_token, set_session


app = Flask(__name__)


# перенести все рендеры в отдельные темлэйты
def render_login_form(args):
    login_form = """
        <body>
            <form action="/dashboard" method="post">
                <p><input name="login" value="login"></p>
                <p><input name="password" value="password"></p>
                <p><input name="ctn" value="phone number"></p>
                <p><button>Welcome!</button></p>
            </form>
        </body>
    """
    if not args.get('error'):        
        body = login_form
    else:
        err_message = args.get('error')
        body = "<h1 style='color: red'>%s</h1><p></p>" % err_message + login_form
    return body


@app.route('/login')
def login():
    body = render_login_form(request.args)
    response = make_response(body)
    set_token(response)
    return response

# перенести все рендеры в отдельные темлэйты
def render_dashboard_page(user_info, subscriptions):
    try:
        template = """
            <h2>Добро пожаловать, %(firstName)s %(lastName)s!</h2>
            <p><b>Ваш адрес:</b> <i>%(invoiceAddr)s</i></p>
            <p><center><h1 style='color: red'>Я слежу за тобой! =^_^= </h1></center></p>
        """
        body = template % user_info
        body += """
            <p>Ваши подписки:</p>
            <p>%s</p>
        """ % subscriptions
        return body
    except (KeyError, ValueError):
        template = """
            <h2>%S</h2>
        """ % user_info
        body = template
        return body



@app.route("/dashboard", methods=['POST'])
def dashboard(): 

    token = request.cookies.get('token')
    if not check_token(token):
        return redirect(url_for('login', error='Включите куки!'))

    # получаем параметры из пришедшего поста
    ctn = request.form.get('ctn')
    login = request.form.get('login')
    password = request.form.get('password')

    # получаем токен или ошибку (пример токена 51BF96B928C8C71124BE61C1BF787B23)
    beeline_token, error_message = get_beeline_token(login, password)

    if not beeline_token:
        return redirect(url_for('login', error=error_message))
    else:
        session = Session(beeline_token, login, ctn)
        set_session(session, token)
        user_info, error_message = get_personal_info(beeline_token, login, ctn)        
        if not user_info:
            user_info = error_message



        subscriptions = get_subscribes(beeline_token, ctn)
        response = render_dashboard_page(user_info, subscriptions)
        return response
