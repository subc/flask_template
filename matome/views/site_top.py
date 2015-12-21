# -*- coding: utf-8 -*-
import random

from flask import render_template, Blueprint
from module.site.site import Site
from views.view_util import err

app = Blueprint("site_top",
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは {{ url_for('site_top.index') }}
@app.route("/")
@err
def index():
    """
    全てのサイトのトップページ
    """
    sites = Site.get_all()
    random.shuffle(sites)
    name = 'ゲーム速報（肉）'
    return render_template('site_top/index.html',
                           sites=sites,
                           name=name)
