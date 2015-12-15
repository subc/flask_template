# -*- coding: utf-8 -*-
import os

from views import root, report
from flask import Flask


def create_app(config=None):
    app = Flask(__name__)

    # config
    if config is None:
        config = os.path.join(app.root_path, 'config/config_local.py')

    app.config.from_pyfile(config)
    app.debug = app.config.get('debug')

    # 機能毎のURLを定義
    app.register_blueprint(root.app, url_prefix="/")
    app.register_blueprint(report.app, url_prefix="/report")

    return app
