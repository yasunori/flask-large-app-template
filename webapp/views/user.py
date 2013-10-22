import sys
import os
from functools import wraps
from flask import Blueprint, render_template, redirect, request, g
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
from webapp.models.users import UsersManager

app = Blueprint(__name__, "user")


def user_login_check(f):
    @wraps(f)
    def _(*args, **kwargs):
        session = request.environ['beaker.session']
        if session.get('user_id', None) is None:
            return redirect('/login/')
        # あとでも使うはずなのでgに入れておく
        user_id = session['user_id']
        usersManager = UsersManager()
        user = usersManager.select_one(user_id)
        g.user = user
        return f(*args, **kwargs)
    return _


@app.route("/", methods=['GET', 'POST'])
@user_login_check
def index():
    dt = {}
    dt['login_id'] = g.user.login_id
    return render_template("user/index.html", dt=dt)


@app.route("/logout/", methods=['GET', 'POST'])
@user_login_check
def logout():
    session = request.environ['beaker.session']
    session['user_id'] = None
    return redirect('/')
