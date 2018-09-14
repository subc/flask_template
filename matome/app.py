# -*- coding: utf-8 -*-
import os
import threading
import logging
from logging.handlers import RotatingFileHandler
from views import root, dat, site_top, sitemap, vote, image
from flask import Flask

tls = threading.local()


def create_app(config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config)

    # 機能毎のURLを定義
    app.register_blueprint(site_top.app, url_prefix="/")
    app.register_blueprint(sitemap.app, url_prefix="/sitemap")
    app.register_blueprint(image.app, url_prefix="/img")
    app.register_blueprint(vote.app, url_prefix="/vote")
    app.register_blueprint(root.app, url_prefix="/<site_title>")
    app.register_blueprint(dat.app, url_prefix="/<site_title>/dat")

    # log
    handler = RotatingFileHandler('/tmp/log/error.log', maxBytes=1024 * 1024 * 10, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    return app


def conf():
    return create_app().config
