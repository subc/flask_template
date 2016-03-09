# -*- coding: utf-8 -*-
from flask import render_template, Blueprint
import logging

# 第一引数の名称が、テンプレのurl_for内で呼び出すときの名称と紐づく
from module.site.exceptions import SiteEmptyError
from module.view_manager.view_util import generate_index_contents
from utils.app_log import app_log
from views.decorator import requires_site_title, err
from views.errorpage import error_page, ErrorPageCategory

app = Blueprint("index",
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは {{ url_for('index.index', site_title=site.title) }}
@app.route("/")
@err
@requires_site_title
def index(site):
    """
    各サイト毎のトップページ
    """
    try:
        svm = generate_index_contents(site)
    except SiteEmptyError:
        app_log(logging.WARNING, "site is empty site_id:{}".format(site.id))
        return error_page(site, ErrorPageCategory.SiteIsEmpty)

    return render_template('root/index.html',
                           svm=svm,
                           site=site)
