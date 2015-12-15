# -*- coding: utf-8 -*-
import os
import threading

from views import root, report
from flask import Flask

tls = threading.local()


def create_app(config=None):
    app = Flask(__name__)

    # configをtlsに保存して、2回目以降呼び出したときにもmanage.pyで指定したconfigにアクセスする
    if config:
        tls.config_path = config
    if hasattr(tls, "config_path"):
        config_path = tls.config_path
        config = os.path.join(app.root_path, config_path)

    # config未設定のときはdefault configを読む
    if config is None:
        config = os.path.join(app.root_path, 'config/config_local.py')

    app.config.from_pyfile(config)
    app.debug = app.config.get('debug')

    # 機能毎のURLを定義
    app.register_blueprint(root.app, url_prefix="/")
    app.register_blueprint(report.app, url_prefix="/report")

    return app
