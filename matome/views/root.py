# -*- coding: utf-8 -*-
import datetime
from flask import render_template, Blueprint

# 第一引数の名称が、テンプレのurl_for内で呼び出すときの名称と紐づく
from module.site.page import Page
from module.site.site import Site

app = Blueprint("index",
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは url_for('index.index')
@app.route("/")
def index():
    import random
    pages = Page.objects().filter().all()
    page = random.choice(pages)
    front_pages = [random.choice(pages) for x in range(6)]
    print(type(page.page))
    site = Site.get(1)
    context = {
        'page': page,
        'site': site,
    }
    print(page.created_at + datetime.timedelta(hours=8))
    return render_template('root/index.html',
                           page=page,
                           site=site,
                           front_pages=front_pages)
