# -*- coding: utf-8 -*-
import sys
import os
from flask import Blueprint, render_template, redirect, request, abort
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
from webapp.forms.regist import RegistForm
from webapp.models.users import UsersManager, Users
from webapp.models.models import DBException

app = Blueprint(__name__, "regist")


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = RegistForm(request.form)
        try:
            varet = form.validate()
        except DBException:
            abort(500)
        if varet:
            usersManager = UsersManager()
            user = Users({'login_id': form.login_id.data,
                          'password': form.password.data})
            try:
                usersManager.insert(user)
                usersManager.commit()
            except DBException:
                abort(500)  # 登録に失敗

            # ログインさせる
            session = request.environ['beaker.session']
            session['user_id'] = user.id
            return redirect('/user/')
        else:
            return render_template("regist/index.html", form=form)
    else:
        form = RegistForm()
        return render_template("regist/index.html", form=form)
