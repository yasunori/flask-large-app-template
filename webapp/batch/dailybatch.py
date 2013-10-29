# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
from main import app
from webapp.models.users import UsersManager, Users
from webapp.models.models import DBException
import logging

import config
app.config.update(config.get_app_conf(config.MODE))
config.set_log_conf(config.MODE)

with app.app_context():
    usersManager = UsersManager()
    dt = {'login_id': 'あまちゃん',
          'password': 'じぇじぇじぇ'}
    #obj = usersManager.insert(dt)
    #usersManager.commit()
    #sys.exit()
    try:
        ret = usersManager.select_one('a')
        print(ret.login_id)
        print(ret.password)
    except DBException as e:
        print("kita")
        print(e)
        pass

    where = (Users.id.in_([1, 2, 3])) & (Users.login_id == 'omochi2')
    print(where)
    where = Users.id.in_([1, 2, 3])
    print(where)
    where = Users.login_id == 'abcd'
    print(where)
    #orderby = "id desc"
    #ret = usersManager.check_exists
