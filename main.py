# -*- coding: utf-8 -*-
from flask import Flask, render_template
from beaker.middleware import SessionMiddleware
import config

app = Flask(__name__, template_folder='webapp/templates', static_folder='webapp/static')

# 各機能を登録
from webapp.views import root
app.register_blueprint(root.app, url_prefix="/")

from webapp.views import login
app.register_blueprint(login.app, url_prefix="/login")

from webapp.views import regist
app.register_blueprint(regist.app, url_prefix="/regist")

from webapp.views import user
app.register_blueprint(user.app, url_prefix="/user")


# エラーハンドラの設定
@app.errorhandler(404)
def page_not_found(error):
    return render_template('common/error.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('common/error.html'), 500


# 起動
if __name__ == '__main__':
    app.config.update(config.get_app_conf(config.MODE))
    config.set_log_conf(config.MODE)
    app.wsgi_app = SessionMiddleware(app.wsgi_app, config.get_app_conf(config.MODE)['SESSION_OPTIONS'])
    app.run(host='0.0.0.0')
