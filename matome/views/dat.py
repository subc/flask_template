# -*- coding: utf-8 -*-
import logging
import random

import datetime

import pytz
from flask import Module, render_template, Blueprint

from module.site.keyword import Keyword
from module.site.page import Page, PageViewLevel
from module.site.page_keyword import PageKeywordRelation
from module.view_manager.view_util import generate_index_contents
from utils.app_log import app_log
from views.decorator import requires_site_title, err
from views.errorpage import error_page, ErrorPageCategory

app = Blueprint('dat',
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは {{ url_for('dat.index', site_title=site.title, page_id=page.id) }}
@app.route('/<page_id>', methods=['GET'], strict_slashes=False)
@err
@requires_site_title
def index(site, page_id):
    # パラメータチェックとメインコンテンツ生成
    page_id = int(page_id)
    try:
        contents = Page.get_by_site(page_id, site.id)
    except Page.DoesNotExist:
        app_log(logging.ERROR, "Page does not exist site_id:{} page_id:{}".format(site.id, page_id))
        return error_page(site, ErrorPageCategory.DoesNotExist)

    # ページが有効期間外ならエラー
    if not contents.is_enable(datetime.datetime.now(pytz.utc)):
        app_log(logging.ERROR, "Page is not open site_id:{} page_id:{}".format(site.id, page_id))
        return error_page(site, ErrorPageCategory.NotOpen)

    # 追加用ページ
    extend_page = contents.get_history_from_myself()
    if contents and contents.prev_page:
        ignore_ids = [page_id, contents.prev_page.id]
    else:
        ignore_ids = [page_id]
    svm = generate_index_contents(site, extend_page=extend_page, ignore_ids=ignore_ids)

    # pvを記録
    if random.randint(0, 20) == 1:
        contents.count_up(20)

    return render_template('dat/page.html',
                           contents=contents,
                           site=site,
                           svm=svm)


@app.route('/matome/<keyword_id>/<start_keyword_id>', methods=['GET'], strict_slashes=False)
@err
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

    # pageのランク付け
    pages = page_rank(pages)

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
@err
@requires_site_title
def history(site, start_page_id):
    """
    過去ログ
    """
    _limit = 20
    svm = generate_index_contents(site)

    # パラメータチェック
    start_page_id = int(start_page_id)
    if start_page_id == 100000000:
        pages = Page.get_new_history(site_id=site.id, _limit=_limit)
    else:
        pages = Page.get_history(site_id=site.id, pk_until=start_page_id, _limit=_limit)

    # pageのランク付け
    pages = page_rank(pages)

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


def page_rank(pages):
    # view数が一定値以下なら何もしない
    if sum([p.view_count for p in pages]) < 10:
        return pages

    # view数でソート
    pages = sorted(pages, key=lambda x: x.view_count, reverse=True)

    # 残りページをView数をベースに点数付与
    for page in pages[0:2]:  # 2件
        page.set_view_level(PageViewLevel.SUPERNOVA)

    for page in pages[2:4]:  # 2件
        page.set_view_level(PageViewLevel.HOT)

    for page in pages[4:6]:  # 2件
        page.set_view_level(PageViewLevel.WARM)

    # 残りをidで降順ソートする
    pages = sorted(pages, key=lambda x: x.id, reverse=True)
    return pages
