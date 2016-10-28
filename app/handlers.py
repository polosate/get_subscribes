from flask import Flask, abort, request, redirect, url_for, make_response, render_template, flash, g, session
from beeline_api.rest_api import get_subscribes
# from auth.session import set_token, get_session, authorization
from app.forms import LoginForm
from app import app, db, lm, oid
from app.models import User, Ctn
from flask_login import login_user, logout_user, current_user, login_required

# перенести все рендеры в отдельные темлэйты
def render_login_form(args, form, providers):
    return render_template('login.html', form=form, title = 'Home', error=args.get('error'), providers=providers)


# перенести все рендеры в отдельные темлэйты
def render_dashboard_page(subscriptions_list=None, subscriptions_str = None, errors=None):
    return render_template('dashboard.html', subscriptions_list=subscriptions_list, \
        subscriptions_str = subscriptions_str,errors=errors)


@app.before_request
def before_request():
    g.user = current_user


def global_ctns():
    ctns = Ctn.query.all()
    
    ctn_list = list(ctn for ctn in ctns)
    global_ctn = list(ctn.ctn for ctn in ctn_list)
    return global_ctn


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
@oid.loginhandler
def login():
    print('START!!!!!')
    if request.method == 'GET':
            form = LoginForm()
            return render_login_form(request.args, form, providers = app.config['OPENID_PROVIDERS'])
    
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()

    if not form.validate_on_submit(): 
        ctn = form.ctn1.data
        ctn_list = global_ctns()
        if not ctn in ctn_list:
            return redirect(url_for('login', error="Номера нет в базе"))  
        session['ctn'] = ctn
        session['remember_me'] = form.remember_me.data
       
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])


    # return render_template('login.html', 
    #   title = 'Sign In',
    #   form = form,
    #   providers = app.config['OPENID_PROVIDERS'])

    # return render_login_form(request.args, form, providers = app.config['OPENID_PROVIDERS'])


@app.route('/login', methods=['POST', 'GET'])
def registration(): pass



@oid.after_login
def after_login(resp):
    if 'ctn' in session:
        ctn = session['ctn']
        print()
    if resp.email is None or resp.email == "":
        print(resp.nickname, resp.email)
        # flash('Invalid login. Please try again.')
        print("Застряли тут!!!")
        return redirect(url_for('login', error='Invalid login. Please try again.'))
    user = User.query.filter_by(email = resp.email).first()
    print(user)
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, ctn = ctn)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('dashboard'))
    # return redirect(url_for('dashboard'))
    


@app.route("/dashboard")
@login_required
def dashboard(): 
        # token = request.cookies.get('token')
        # session = get_session(token)
        # if not session:
        #     return redirect(url_for('login', error="Аутентифицируйтесь, блеа!"))

        # beeline_token = session.beeline_token
        # ctn = session.get_ctn()

        # subscriptions, errors = get_subscribes(beeline_token, ctn)

        # if not errors:
        #     if isinstance(subscriptions, list):
        #         response = render_dashboard_page(subscriptions_list = subscriptions)
        #     else:
        #         response = render_dashboard_page(subscriptions_str = subscriptions)
        # else:
        #     response = render_dashboard_page(errors = errors)

        return 'response'


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
