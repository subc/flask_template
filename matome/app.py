# -*- coding: utf-8 -*-
import os
import threading
import logging
from logging.handlers import RotatingFileHandler
from views import root, dat, site_top, sitemap
from flask import Flask

tls = threading.local()


def create_app(config=None):
    app = Flask(__name__, static_url_path='/static')

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
    app.register_blueprint(site_top.app, url_prefix="/")
    app.register_blueprint(sitemap.app, url_prefix="/sitemap")
    app.register_blueprint(root.app, url_prefix="/<site_title>")
    app.register_blueprint(dat.app, url_prefix="/<site_title>/dat")

    # log
    handler = RotatingFileHandler('/tmp/log/error.log', maxBytes=1024 * 1024 * 10, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    return app


def conf():
    return create_app().config
