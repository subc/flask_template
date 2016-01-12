# -*- coding: utf-8 -*-
import random

import datetime

import pytz

from module.site.page import Page, PageViewLevel
from module.site.site import Site
from utils.tls_property import cached_tls


class SiteViewModel(object):
    """
    ページ表示用データを生成するためのベースの型
    """
    def __init__(self, site, contents, panels, page_list):
        self.site = site
        self.contents = contents
        self.panels = panels
        self.page_list = page_list


def generate_index_contents(site, _limit=30, extend_page=None, ignore_ids=()):
    """
    トップページ表示用のデータを生成する
    :param site: Site
    :param _limit: int
    :param extend_page: list(Page)
    :param ignore_ids: list(int)
    :return: SiteViewModel
    """
    pages = Page.get_new_history(site.id, _limit=_limit)
    if extend_page:
        pages += extend_page

    # 未来日公開の記事は公開しない
    now = datetime.datetime.now(pytz.utc)
    pages = [page for page in pages if page.is_enable(now=now)]

    if ignore_ids:
        pages_repository = {page.id: page for page in pages if page.id not in ignore_ids}
    else:
        pages_repository = {page.id: page for page in pages}
    pages = list(pages_repository.values())

    # 10件未満
    if len(pages) <= 10:
        pr_pages = get_pr_page(site)
        return SiteViewModel(site=site,
                             contents=random.choice(pages),
                             panels=[random.choice(pages) for x in range(6)],
                             page_list=pages + pr_pages)

    # 最新の10件からviewが多い1件を取る
    new_list = sorted(pages, key=lambda x: x.id, reverse=True)[:10]
    new_list = sorted(new_list, key=lambda x: x.view_count, reverse=True)
    if len(new_list) == len([page for page in new_list if page.start_at]):
        new_list = sorted(new_list, key=lambda x: x.start_at, reverse=True)
    contents = new_list[0]
    new_list = new_list[1:]
    pages_repository.pop(contents.id)

    # 人気順に並んだ最新の9件からパネル用の3件を取る
    random.shuffle(new_list)
    panels = new_list[1:4]
    for panel_page in panels:
        panel_page.set_favorite(False)
        pages_repository.pop(panel_page.id)

    # 残りの46件からviewが多い3件を取る
    left_pages = list(pages_repository.values())
    left_pages = sorted(left_pages, key=lambda x: x.view_count, reverse=True)
    for x in range(3):
        panel_page = left_pages.pop()
        panel_page.set_favorite(True)
        panels.append(panel_page)
    random.shuffle(panels)

    # 残りページをView数をベースに点数付与
    for page in left_pages[0:3]:  # 3件
        page.set_view_level(PageViewLevel.SUPERNOVA)

    for page in left_pages[3:5]:  # 2件
        page.set_view_level(PageViewLevel.HOT)

    for page in left_pages[5:7]:  # 2件
        page.set_view_level(PageViewLevel.WARM)

    # 残りをidで降順ソートする
    left_pages = sorted(left_pages, key=lambda x:x.id, reverse=True)

    # クローラー用のPRページを追加
    left_pages += get_pr_page(site)
    return SiteViewModel(site=site,
                         contents=contents,
                         panels=panels,
                         page_list=left_pages)


def get_pr_page(site, _limit=3):
    """
    クローラー最適化のために、外部サイトのページを取得する
    :param site: site
    :return: list[Page]
    """
    other_site = _get_other_site(site)
    pages = Page.get_new_history(other_site.id, _limit=30)
    pages = sorted(pages, key=lambda x: x.view_count, reverse=True)
    result = []
    now = datetime.datetime.now(pytz.utc)
    for page in pages:
        if page.is_enable(now):
            result.append(page)
        if len(result) >= _limit:
            return result
    return result


def _get_other_site(site):
    all_site = Site.get_all()
    for x in range(100):
        _site = random.choice(all_site)
        if _site.id != site.id:
            return _site
    raise ValueError
