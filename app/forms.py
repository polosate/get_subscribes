from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, DateField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from wtforms import validators
from app.models import User, is_phone_number_exists, is_user_registrated, is_login_exists


def is_ctn_exists(form, field):
    if not is_phone_number_exists(field.data):
        raise ValidationError('Unknown phone number')


def is_login_busy(form, field):
    if is_login_exists(field.data):
        raise ValidationError('Username already busy')


def is_user_exists(form, field):
    if not is_user_registrated(field.data):
        raise ValidationError('User is not registrated')


def is_user_not_exists(form, field):
    if is_user_registrated(field.data):
        raise ValidationError('User already exists')


def date_validator(form, field):
    pass


class LoginForm(Form):
    ctn1 = TextField('ctn1', validators=[DataRequired(), is_user_exists])
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    # remember_me = BooleanField('remember_me', default = False)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False        

        username = User.query.filter_by(username=self.username.data).first()
        if not username:
            self.username.errors.append('Unknown username')
            return False

        password = User.query.filter_by(password = self.password.data).first()
        if not password:
            self.password.errors.append('Invalid password')
            return False

        user = User.query.filter_by(username = self.username.data).filter_by(ctn = self.ctn1.data).first()
        if not user:
            self.password.errors.append('Invalid username or phone number')
            return False

        return True


class RegistrationForm(Form):
    ctn1 = TextField('ctn1', validators = [DataRequired(), is_ctn_exists, is_user_not_exists])
    username = TextField('username', validators = [DataRequired(), is_login_busy])
    password = PasswordField('password', validators = [DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('confirm', validators = [DataRequired()])
    email = TextField('email')


class AskPhoneForm(Form):
    ctn1 = TextField('ctn1', validators=[DataRequired(), is_ctn_exists, is_user_not_exists])


class EditProfile(Form):
    ctn1 = TextField('ctn1', validators=[DataRequired(), is_ctn_exists])
    year = TextField('year')
    month = TextField('month')
    day = TextField('day')
    about_me = TextAreaField('about_me')
