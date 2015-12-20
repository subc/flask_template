# -*- coding: utf-8 -*-
from flask import render_template, Blueprint

# 第一引数の名称が、テンプレのurl_for内で呼び出すときの名称と紐づく
from module.site.site import Site
from module.view_manager.view_util import generate_index_contents
from views.view_util import requires_site_title

app = Blueprint("site_top",
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは {{ url_for('site_top.index') }}
@app.route("/")
def index():
    """
    全てのサイトのトップページ
    """
    sites = Site.get_all()
    name = 'ゲーム速報（肉）'
    return render_template('site_top/index.html',
                           sites=sites,
                           name=name)
