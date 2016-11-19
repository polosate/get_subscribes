from flask import request, redirect, url_for, render_template, \
    flash, g, session

from beeline_api.rest_api import get_subscriptions, remove_subscriptions
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm, AskPhoneForm, \
    EditProfile, is_phone_number_exists
from app import app, db
from app.models import User

from celeryapp.tasks import check_subscriptions


def render_dashboard_page(
        subscriptions_list=None,
        subscriptions_str=None,
        errors=None
):
    return render_template(
        'dashboard.html',
        subscriptions_list=subscriptions_list,
        subscriptions_str=subscriptions_str,
        errors=errors
    )


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', username=current_user.username)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
            form = LoginForm()
            return render_template(
                'login.html',
                form=form,
                title='Home',
                error=request.args.get('error')
            )

    if g.user is not None and g.user.is_authenticated:
        return redirect(request.args.get('next') or  url_for('dashboard'))

    form = LoginForm(request.form)
    is_form_valid = form.validate()

    if is_phone_number_exists(form.ctn1.data):
        session['ctn'] = form.ctn1.data

    if is_form_valid:
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).filter_by(password=password).first()
        login_user(user),
        return redirect(request.args.get('next') or url_for('dashboard'))

    return render_template(
        'login.html',
        form=form,
        title='Home',
        error=request.args.get('error'))


@app.route('/askphone', methods=['POST', 'GET'])
def askphone():

    username = g.user.username
    if not User.query.filter_by(username=username).first().ctn:

        if request.method == 'GET':
            form = AskPhoneForm()
            return render_template('askphone.html', form=form, title='Phone')


        form = AskPhoneForm(request.form)
        is_form_valid = form.validate()

        if is_form_valid:
            ctn = form.ctn1.data
            user = User.query.filter_by(username=username).first()
            user.ctn = ctn
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(request.args.get('next') or url_for('dashboard'))
        return render_template('askphone.html', form=form)

    return redirect(request.args.get('next') or url_for('dashboard'))


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if 'ctn' in session:
        ctn = session['ctn']
    else:
        ctn = None

    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('registration.html', form=form, title='Registration', ctn=ctn)

    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm(request.form)
    is_form_valid = form.validate()

    if is_form_valid:
        username = form.username.data
        password = form.password.data
        ctn = form.ctn1.data
        email = form.email.data

        user = User(username=username, password=password, ctn=ctn, email = email)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(request.args.get('next') or url_for('dashboard'))
    return render_template('registration.html', form=form, title = 'Registration')


def get_ctn_for_current_user():
    if 'ctn' not in session:
        session['ctn'] =  User.query.filter_by(username=g.user.username).first().ctn
        print(session['ctn'])
    return session['ctn']

@app.route("/dashboard", methods=['POST', 'GET'])
@login_required
def dashboard():
    ctn = get_ctn_for_current_user()
    if request.method == "POST":
        # subscriptionId = request.args.get("subscriptionId")
        subscriptionId = request.form['subscriptionId']
        response_message = remove_subscriptions(ctn, subscriptionId)
        res = check_subscriptions.delay(db, ctn, subscriptionId, g.user.id)

        return redirect(url_for('dashboard'))

    subscriptions, errors = get_subscriptions(ctn)

    if not errors:
        if isinstance(subscriptions, list):
            response = render_dashboard_page(subscriptions_list = subscriptions)
        else:
            response = render_dashboard_page(subscriptions_str = subscriptions)
    else:
        response = render_dashboard_page(errors = errors)
    return response


@app.route('/user/<username>')
@login_required
def user(username):
    if current_user.username != username:
        flash('Bad credentials. You sre not logged In as ' + username )
        return redirect(url_for('user', username=current_user.username))
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('User ' + username + ' not found.')
        return redirect(url_for('index'))
    return render_template('user.html', username=username)



@app.route('/edit/<username>', methods=['POST', 'GET'])
@login_required
def edit(username):
    user = User.query.filter_by(username=username).first()

    if request.method == 'GET':
        form = EditProfile()
        form.about_me.data=user.about_me
        return render_template('edit.html', form=form, title='Edit profile', user=current_user)
    else:
        form = EditProfile(request.form)
        #is_form_valid = form.validate()

        user.ctn = form.ctn1.data
        user.birth_day = form.birth_day.data
        user.about_me = form.about_me.data
        db.session.commit()

        return render_template('user.html', user=user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
