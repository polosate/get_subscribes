from flask import Flask, abort, request, redirect, url_for, make_response, render_template
from beeline_api.rest_api import get_subscribes
from auth.session import set_token, get_session, authorization
from .app import app


# перенести все рендеры в отдельные темлэйты
def render_login_form(args):
    return render_template('login.html', error=args.get('error'))


# перенести все рендеры в отдельные темлэйты
def render_dashboard_page(subscriptions_list=None, subscriptions_str = None, errors=None):
    return render_template('dashboard.html', subscriptions_list=subscriptions_list, \
        subscriptions_str = subscriptions_str,errors=errors)


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        body = render_login_form(request.args)
        response = make_response(body)
        set_token(response)
        return response
    else:
        return authorization(request)


@app.route("/dashboard")
def dashboard(): 
        token = request.cookies.get('token')
        session = get_session(token)
        if not session:
            return redirect(url_for('login', error="Аутентифицируйтесь, блеа!"))

        beeline_token = session.beeline_token
        ctn = session.get_ctn()

        subscriptions, errors = get_subscribes(beeline_token, ctn)

        if not errors:
            if isinstance(subscriptions, list):
                response = render_dashboard_page(subscriptions_list = subscriptions)
            else:
                response = render_dashboard_page(subscriptions_str = subscriptions)
        else:
            response = render_dashboard_page(errors = errors)

        return response
