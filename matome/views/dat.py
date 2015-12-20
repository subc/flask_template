# -*- coding: utf-8 -*-
import random

from flask import Module, render_template, Blueprint

from module.site.keyword import Keyword
from module.site.page import Page
from module.site.page_keyword import PageKeywordRelation
from module.view_manager.view_util import generate_index_contents
from views.view_util import requires_site_title

app = Blueprint('dat',
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは {{ url_for('dat.index', site_title=site.title, page_id=page.id) }}
@app.route('/<page_id>', methods=['GET'], strict_slashes=False)
@requires_site_title
def index(site, page_id):
    # パラメータチェックとメインコンテンツ生成
    page_id = int(page_id)
    contents = Page.get_by_site(page_id, site.id)
    svm = generate_index_contents(site)

    # pvを記録
    contents.count_up()

    return render_template('dat/page.html',
                           contents=contents,
                           site=site,
                           svm=svm)


@app.route('/matome/<keyword_id>/<start_keyword_id>', methods=['GET'], strict_slashes=False)
@requires_site_title
def keyword(site, keyword_id, start_keyword_id):
    _limit = 20

    # パラメータチェック
    keyword_id = int(keyword_id)
    start_keyword_id = int(start_keyword_id)
    keyword = Keyword.get(keyword_id)
    if start_keyword_id == 100000000:
        relation = PageKeywordRelation.get_from_new_keyword(keyword_id, _limit=_limit)
    else:
        relation = PageKeywordRelation.get_from_keyword(keyword_id, start_keyword_id, _limit=_limit)
    pages = [r.page for r in relation]
    svm = generate_index_contents(site)

    # 次のページの遷移先
    is_next = None
    if relation and len(relation) == _limit:
        last_page_id = relation[-1].id
        is_next = last_page_id - 1

    return render_template('dat/keyword.html',
                           site=site,
                           keyword=keyword,
                           svm=svm,
                           list_pages=pages,
                           is_next=is_next)


@app.route('/history/<start_page_id>', methods=['GET'], strict_slashes=False)
@requires_site_title
def history(site, start_page_id):
    """
    過去ログ
    """
    _limit = 20

    # パラメータチェック
    start_page_id = int(start_page_id)
    if start_page_id == 100000000:
        pages = Page.get_new_history(site_id=site.id, _limit=_limit)
    else:
        pages = Page.get_history(site_id=site.id, pk_until=start_page_id, _limit=_limit)
    svm = generate_index_contents(site)

    # 次のページの遷移先
    is_next = None
    if pages and len(pages) == _limit:
        last_page_id = pages[-1].id
        is_next = last_page_id - 1

    return render_template('dat/history.html',
                           site=site,
                           keyword=keyword,
                           list_pages=pages,
                           svm=svm,
                           is_next=is_next)
