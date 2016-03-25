# -*- coding: utf-8 -*-
"""
画像サンプルをWeb表示
"""
from flask import render_template, Blueprint
import logging

# 第一引数の名称が、テンプレのurl_for内で呼び出すときの名称と紐づく
from module.site.exceptions import SiteEmptyError
from module.site.site import Site
from module.view_manager.view_util import generate_index_contents
from utils.app_log import app_log
from views.decorator import requires_site_title, err
from views.errorpage import error_page, ErrorPageCategory

app = Blueprint("image",
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは {{ url_for('index.index', site_title=site.title) }}
@app.route("/")
@err
def image():
    """
    各サイト毎のトップページ
    """
    site_all = Site.get_all()
    return render_template('image/index.html',
                           site_all=site_all)
