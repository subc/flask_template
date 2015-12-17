# -*- coding: utf-8 -*-
import random

from flask import Module, render_template, Blueprint

from module.site.keyword import Keyword
from module.site.page import Page
from module.site.page_keyword import PageKeywordRelation
from module.site.site import Site
from views.view_util import requires_site_title

app = Blueprint('dat',
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは {{ url_for('dat.index', site_title=site.title, page_id=page.id) }}
@app.route('/<page_id>', methods=['GET'], strict_slashes=False)
@requires_site_title
def index(site, page_id):
    # パラメータチェック
    try:
        page_id = int(page_id)
    except ValueError:
        # todo redirect error page
        return 'error'
    contents = Page.get(page_id)
    if contents is None:
        # todo error
        return 'page id does not exist error'

    # pvを記録
    contents.count_up()

    # todo dummy
    site = Site.get(1)
    pages = Page.objects().filter().all()
    panel_pages = [random.choice(pages) for x in range(6)]

    return render_template('dat/page.html',
                           contents=contents,
                           site=site,
                           panel_pages=panel_pages)


# テンプレート内で呼び出すときは {{ url_for('dat.keyword', site_title=site.title, keyword_id=keyword.id) }}
# @app.route('/matome/<keyword_id>', methods=['GET'], strict_slashes=False)
# @requires_site_title
# def keyword(site, keyword_id):
#     _limit = 20
#     # パラメータチェック
#     try:
#         keyword_id = int(keyword_id)
#         keyword = Keyword.get(keyword_id)
#         relation = PageKeywordRelation.get_from_new_keyword(keyword_id, _limit=_limit)
#         pages = [r.page for r in relation]
#     except ValueError:
#         # todo redirect error page
#         return 'error'
#
#     # todo dummy
#     page_all = Page.objects().filter().all()
#     panel_pages = [random.choice(page_all) for x in range(6)]
#
#     # todo dummy 色つける
#     if pages:
#         for x in range(4):
#             _ = random.choice(pages)
#             _.set_color_supernova()
#         for x in range(5):
#             _ = random.choice(pages)
#             _.set_color_hot()
#
#     # 次のページの遷移先
#     is_next = None
#     if relation and len(relation) == _limit:
#         last_page_id = relation[-1].id
#         is_next = last_page_id - 1
#
#     return render_template('dat/keyword.html',
#                            site=site,
#                            keyword=keyword,
#                            panel_pages=panel_pages,
#                            list_pages=pages,
#                            is_next=is_next)


@app.route('/matome/<keyword_id>/<start_keyword_id>', methods=['GET'], strict_slashes=False)
@requires_site_title
def keyword(site, keyword_id, start_keyword_id):
    _limit = 20

    # パラメータチェック
    try:
        keyword_id = int(keyword_id)
        start_keyword_id = int(start_keyword_id)
        keyword = Keyword.get(keyword_id)
        relation = PageKeywordRelation.get_from_keyword(keyword_id, start_keyword_id, _limit=_limit)
        pages = [r.page for r in relation]
    except ValueError:
        # todo redirect error page
        return 'error'

    # todo dummy
    page_all = Page.objects().filter().all()
    panel_pages = [random.choice(page_all) for x in range(6)]

    # todo dummy 色つける
    if pages:
        for x in range(4):
            _ = random.choice(pages)
            _.set_color_supernova()
        for x in range(5):
            _ = random.choice(pages)
            _.set_color_hot()

    # 次のページの遷移先
    is_next = None
    if relation and len(relation) == _limit:
        last_page_id = relation[-1].id
        is_next = last_page_id - 1

    return render_template('dat/keyword.html',
                           site=site,
                           keyword=keyword,
                           panel_pages=panel_pages,
                           list_pages=pages,
                           is_next=is_next)
