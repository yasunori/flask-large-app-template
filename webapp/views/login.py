# -*- coding: utf-8 -*-
import cgi
import urllib
import json
import sys
import os
from flask import Blueprint, render_template, redirect, request, current_app, abort
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
from webapp.forms.login import LoginForm
from webapp.models.users import UsersManager, Users
from webapp.lib import facebook
#import logging

app = Blueprint(__name__, 'login')


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            usersManager = UsersManager()
            where = (Users.login_id == form.login_id.data)
            users = usersManager.select(where)
            # ログイン処理
            session = request.environ['beaker.session']
            session['user_id'] = users[0].id
            #return redirect(url_for('user.index'))
            return redirect('/user/')
        else:
            return render_template('login/index.html', form=form)
    else:
        form = LoginForm()
        return render_template('login/index.html', form=form)


@app.route("/facebook", methods=['GET', 'POST'])
def facebooklogin():
    verification_code = request.args.get('code')
    args = dict(client_id='167537889944255',
                redirect_uri=request.url)
    if verification_code:
        args["client_secret"] = '96044a6e828ebb3393dac25bfc894cb4'
        args["code"] = verification_code
        response = cgi.parse_qs(urllib.urlopen(
                "https://graph.facebook.com/oauth/access_token?" +
                urllib.urlencode(args)).read())
        access_token = response["access_token"][-1]
        response = urllib.urlopen(
                "https://graph.facebook.com/me?" +
                urllib.urlencode(dict(access_token=access_token))).read()

        profile = json.load(urllib.urlopen(
                "https://graph.facebook.com/me?" +
                urllib.urlencode(dict(access_token=access_token))))

        #graph = facebook.GraphAPI(access_token) # コメントを外すと書き込みに行く
        #graph.put_wall_post('テスト'.encode('utf-8')) # facebook sdk はバイト列を期待してたから
        return render_template("login/facebook.html", profile=profile)
    else:
        return redirect(
            "https://graph.facebook.com/oauth/authorize?" +
            urllib.urlencode(args))
