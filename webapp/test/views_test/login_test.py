# -*- coding: utf-8 -*-
import sys
import os
from beaker.middleware import SessionMiddleware
from nose.tools import ok_, eq_
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../')
import config
config.set_mode('TESTING')  # テストモードに切り替え
import main
from webapp.models import database
from webapp.models.users import UsersManager

client = None


def setup():
    global client
    tmp_app = main.app
    conf = config.get_app_conf(config.MODE)
    tmp_app.config.update(conf)
    tmp_app.wsgi_app = SessionMiddleware(tmp_app.wsgi_app, conf['SESSION_OPTIONS'])
    client = tmp_app.test_client()

    # データの準備
    database.clear_db()
    database.init_db()
    usersManager = UsersManager()
    usersManager.insert({'login_id': 'abcd',
                         'password': '12345678'})


def index_test():
    global client
    # 表示
    rv = client.get('/login/')
    ok_('ログイン' in rv.data.decode('UTF-8'))

    # 正常系
    rv = client.post('/login/', data={'login_id': 'abcd',
                                   'password': '12345678'}, follow_redirects=True)
    ok_('会員' in rv.data.decode('UTF-8'))

    # ところでセッション生きてる？
    rv = client.get('/user/',follow_redirects=True)
    ok_('会員' in rv.data.decode('UTF-8'))

    # ログアウトします
    rv = client.get('/user/logout/',follow_redirects=True)
    ok_('TOP' in rv.data.decode('UTF-8'))

    # 異常系
    rv = client.post('/login/', data={'login_id': '',
                                   'password': ''}, follow_redirects=True)
    ok_('入力してください' in rv.data.decode('UTF-8'))
