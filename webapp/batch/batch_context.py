# -*- coding: utf-8 -*-
import sys
import os
from flask import render_template, current_app
from flask_mail import Message, Mail
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
from main import app
from webapp.models.users import UsersManager, Users
import logging
from email import charset

import config
app.config.update(config.get_app_conf(config.MODE))
config.set_log_conf(config.MODE)

with app.app_context():
    mail = Mail(current_app)

    #charset.add_charset('utf-8', charset.SHORTEST, None, 'iso-2022-jp')
    charset.add_charset('utf-8', charset.SHORTEST, None, None)
    msg = Message('表題', sender='admin@testtesttest.com',
                  recipients=["yasunori@gotoh.me"], charset='utf-8')
    msg.body = render_template("mail/test.tpl", name='なまえ',
                               free='試験です\n試験だよ')
    #msg.html = html_body

    mail.send(msg)
