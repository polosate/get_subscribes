from flask import Flask, abort, request, redirect, url_for, make_response, render_template, flash, g, session
from beeline_api.rest_api import get_subscribes, get_beeline_token
from app.forms import LoginForm, RegistrationForm, is_phone_number_exists
from app import app, db, lm
from app.models import User, Ctn, get_user
from flask_login import login_user, logout_user, current_user, login_required



def render_dashboard_page(subscriptions_list=None, subscriptions_str = None, errors=None):
    return render_template('dashboard.html', subscriptions_list=subscriptions_list, \
        subscriptions_str = subscriptions_str,errors=errors)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', user=current_user.login)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
            form = LoginForm()
            return render_template('login.html', form=form, title = 'Home', error=request.args.get('error'))

    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm(request.form)
    is_form_valid = form.validate()

    if is_phone_number_exists(form.ctn1.data):
        session['ctn'] = form.ctn1.data
    
    if is_form_valid:
        # ctn = form.ctn1.data
        login = form.login.data
        password = form.password.data
        # session['ctn'] = ctn
        user = User.query.filter_by(login = login).filter_by(password = password).first()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form, title = 'Home', error=request.args.get('error'))


@app.route('/registration', methods=['POST', 'GET'])
def registration(): 
    if 'ctn' in session:
        ctn = session['ctn']
    else:
        ctn = None

    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('registration.html', form=form, title = 'Registration', ctn=ctn)
    
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm(request.form)
    is_form_valid = form.validate()
    print(form.errors)

    if is_form_valid:
        login = form.login.data
        password = form.password.data
        ctn = form.ctn1.data
        
        user = User(login = login, password = password, ctn = ctn)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(request.args.get('next') or url_for('dashboard'))
    return render_template('registration.html', form=form, title = 'Registration')


def get_ctn_for_current_user():
    if 'ctn' not in session:
        session['ctn'] =  User.query.filter_by(login=g.user.login).first().ctn
        print(session['ctn'])
    return session['ctn']

@app.route("/dashboard")
@login_required
def dashboard(): 
    bt, _ = get_beeline_token()
    ctn = get_ctn_for_current_user()

    subscriptions, errors = get_subscribes(bt, ctn)

    if not errors:
        if isinstance(subscriptions, list):
            response = render_dashboard_page(subscriptions_list = subscriptions)
        else:
            response = render_dashboard_page(subscriptions_str = subscriptions)
    else:
        response = render_dashboard_page(errors = errors)

    return response


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
