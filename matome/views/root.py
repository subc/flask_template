# -*- coding: utf-8 -*-
import datetime
from flask import render_template, Blueprint

# 第一引数の名称が、テンプレのurl_for内で呼び出すときの名称と紐づく
from module.site.page import Page
from module.view_manager.view_util import generate_index_contents
from views.view_util import requires_site_title

app = Blueprint("index",
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは {{ url_for('index.index', site_title=site.title) }}
@app.route("/")
@requires_site_title
def index(site):
    svm = generate_index_contents(site)
    raise
    return render_template('root/index.html',
                           svm=svm,
                           site=site)
