from flask_wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    ctn1 = TextField('ctn1', validators = [Required()])
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


class RegistrationForm(Form):
    ctn1 = TextField('ctn1', validators = [Required()])
    login = TextField('login', validators = [Required()])
    password = TextField('password', validators = [Required()])