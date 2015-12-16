# -*- coding: utf-8 -*-
import random

from flask import Module, render_template, Blueprint

from module.site.page import Page
from module.site.site import Site

app = Blueprint('dat',
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは {{ url_for('dat.index', page_id=page.id) }}
@app.route('/<page_id>', methods=['GET'], strict_slashes=False)
def index(site_title, page_id):
    try:
        site = Site.get_title(site_title)
    except IndexError:
        # todo
        return 'error site_title does not exist'

    page_id = 1
    # パラメータチェック
    try:
        page_id = int(page_id)
    except ValueError:
        # todo redirect error page
        return 'error'
    page = Page.get(page_id)
    if page is None:
        # todo error
        return 'page id does not exist error'

    # pvを記録
    page.count_up()

    # todo dummy
    site = Site.get(1)
    pages = Page.objects().filter().all()
    panel_pages = [random.choice(pages) for x in range(6)]

    return render_template('root/index.html',
                           page=page,
                           site=site,
                           panel_pages=panel_pages)
