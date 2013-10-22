# -*- coding: utf-8 -*-
import sys
import os
from flask import Blueprint, render_template, redirect, request
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
from webapp.forms.regist import RegistForm
from webapp.models.users import UsersManager

app = Blueprint(__name__, "regist")


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = RegistForm(request.form)
        if form.validate():
            #c1 = Users('test','abebe')
            usersManager = UsersManager()

            dt = {'login_id': form.login_id.data,
                  'password': form.password.data}
            user = usersManager.insert(dt)

            # ログインさせる
            session = request.environ['beaker.session']
            session['user_id'] = user.id
            return redirect('/user/')
        else:
            return render_template("regist/index.html", form=form)
    else:
        form = RegistForm()
        return render_template("regist/index.html", form=form)
