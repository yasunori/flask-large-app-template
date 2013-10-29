# -*- coding: utf-8 -*-
#from flask_wtf import Form
from wtforms import Form
from wtforms import TextField, PasswordField
from wtforms import validators, ValidationError
from webapp.models.users import UsersManager, Users
from webapp.models.models import DBException


def check_user(form, field):
    '''
    そんなユーザが居るかどうかのチェックをします。
    '''
    where = (Users.login_id == form.login_id.data) & (Users.password == form.password.data)
    usersManager = UsersManager()
    try:
        if not usersManager.select(where):
            raise ValidationError('IDもしくはパスワードが異なります')
    except DBException:
        raise


class LoginForm(Form):
    login_id = TextField('ID', [
        validators.Required(message="入力してください"),
        validators.Length(max=30, message="30文字以内で入力してください")])

    password = PasswordField('パスワード', [
        validators.Required(message="入力してください"),
        check_user])
