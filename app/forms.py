from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required, ValidationError, EqualTo
from app.models import User, Ctn, is_phone_number_exists, is_user_registrated, is_login_exists


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


class LoginForm(Form):
    ctn1 = TextField('ctn1', validators = [Required(), is_user_exists])
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])

    # remember_me = BooleanField('remember_me', default = False)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False        

        username = User.query.filter_by(username = self.username.data).first()
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
    ctn1 = TextField('ctn1', validators = [Required(), is_ctn_exists, is_user_not_exists])
    username = TextField('username', validators = [Required(), is_login_busy])
    password = PasswordField('password', validators = [Required(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('confirm', validators = [Required()])
    email = TextField('email')


class AskPhoneForm(Form):
    ctn1 = TextField('ctn1', validators = [Required(), is_ctn_exists, is_user_not_exists])
