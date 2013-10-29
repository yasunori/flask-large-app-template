# -*- coding: utf-8 -*-
#from flask_wtf import Form
from wtforms import Form
from wtforms import TextField, PasswordField
from wtforms import validators, ValidationError
from webapp.models.users import UsersManager
from webapp.models.models import DBException


def check_exists(form, field):
    '''
    login_idが既に使われているかどうかをチェックする
    '''
    usersManager = UsersManager()
    try:
        if(usersManager.check_exists(login_id=field.data)):
            raise ValidationError('既にあります')
    except DBException:
        raise


class RegistForm(Form):
    login_id = TextField('ID', [
        validators.Required(message="入力してください"),
        validators.Length(max=30, message="30文字以内で入力してください"),
        check_exists])

    password = PasswordField('パスワード', [
        validators.Required(message="入力してください"),
        validators.Length(min=8, max=16, message="8文字以上16文字以内で入力してください"),
        validators.Regexp("^[0-9A-z-_]+$", message="使用できる文字は半角英数字、-（ハイフン）、_(アンダーバー）です")])
