from datetime import date
from flask import request, redirect, url_for, render_template, \
    flash, g, session


from beeline_api.rest_api import get_subscriptions, remove_subscriptions
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm, AskPhoneForm, \
    EditProfile, is_phone_number_exists
from app import app, db
from app.models import User, Tasks

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

def get_ctn_for_current_user():
    if 'ctn' not in session:
        session['ctn'] =  User.query.filter_by(username=g.user.username).first().ctn
        print(session['ctn'])
    return session['ctn']

def add_subscription_status(subscription_list, subscription_id, status):
    for subscription in subscription_list:
        if subscription['id'] == subscription_id:
            subscription['status'] = status


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
        return redirect(request.args.get('next') or url_for('dashboard'))

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


def show_removed_subscriptions(subscription_ids):
    tasks = Tasks.query.filter_by(user_id=g.user.id).all()
    ids = []
    for task in tasks:
        if check_subscriptions.AsyncResult(task.task_id).successful():
            ids.append(task.subscription_id)
            db.session.delete(task)
            db.session.commit()

    removed_sub_id = []
    for id in ids:
        if id not in subscription_ids:
            removed_sub_id.append(id)

    for subs in removed_sub_id:
        flash('Subscription ' + subs + ' removed.')


@app.route("/dashboard", methods=['POST', 'GET'])
@login_required
def dashboard():
    ctn = get_ctn_for_current_user()
    if request.method == "POST":
        subscriptionId = request.form['subscriptionId']
        remove_subscriptions(ctn, subscriptionId)
        res = check_subscriptions.delay(ctn, subscriptionId)
        task = Tasks.query.filter_by(subscription_id=subscriptionId).filter_by(user_id=g.user.id).first()
        if not task:
            task = Tasks(task_id=res.id, subscription_id=subscriptionId, user_id=g.user.id)
        else:
            task.task_id=res.id
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('dashboard'))

    subscriptions, errors = get_subscriptions(ctn)

    if not errors:
        if isinstance(subscriptions, list):
            subscription_status = {'Exists': 0, 'Awaiting removing': 1, 'Removing error': 2}
            subscription_ids = [subscription['id'] for subscription in subscriptions]

            show_removed_subscriptions(subscription_ids)

            for subscription_id in subscription_ids:
                task = Tasks.query.filter_by(subscription_id=subscription_id).filter_by(user_id=g.user.id).first()
                if not task:
                    add_subscription_status(subscriptions, subscription_id,
                                            subscription_status['Exists'])
                else:
                    task_id = task.task_id
                    if not check_subscriptions.AsyncResult(task_id).ready():
                        add_subscription_status(subscriptions, subscription_id,
                                                subscription_status['Awaiting removing'])
                    else:
                        if check_subscriptions.AsyncResult(task_id).failed():
                            add_subscription_status(subscriptions, subscription_id,
                                                    subscription_status['Removing error'])
                        else:
                            add_subscription_status(subscriptions, subscription_id,
                                                    subscription_status['Exists'])
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
        form.about_me.data = user.about_me
        return render_template('edit.html', form=form, title='Edit profile', user=current_user)
    else:
        form = EditProfile(request.form)
        is_form_valid = form.validate()
        if is_form_valid:
            user.ctn = form.ctn1.data
            user.birth_day = date(int(form.year.data), int(form.month.data), int(form.day.data))
            user.about_me = form.about_me.data
            db.session.commit()
            return render_template('user.html', user=user)
        else:
            return render_template('edit.html', form=form, title='Edit profile', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
