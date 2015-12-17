# -*- coding: utf-8 -*-
import datetime
from flask import render_template, Blueprint

# 第一引数の名称が、テンプレのurl_for内で呼び出すときの名称と紐づく
from module.site.page import Page
from views.view_util import requires_site_title

app = Blueprint("index",
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは {{ url_for('index.index', site_title=site.title) }}
@app.route("/")
@requires_site_title
def index(site):
    import random
    pages = Page.get_new_history(site.id, _limit=12)
    contents = random.choice(pages)
    panel_pages = [random.choice(pages) for x in range(6)]

    # for debug
    # for page in pages:
    #     print(page.keywords, page.tile_label, page.keyword_top)

    return render_template('root/index.html',
                           contents=contents,
                           site=site,
                           panel_pages=panel_pages,
                           list_pages=pages)
