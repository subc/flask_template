# -*- coding: utf-8 -*-
import random

from module.site.page import Page, PageViewLevel
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


def generate_index_contents(site):
    """
    トップページ表示用のデータを生成する
    :param site: Site
    :return: SiteViewModel
    """
    pages = Page.get_new_history(site.id, _limit=50)
    pages_repository = {page.id: page for page in pages}

    # 50件未満
    if len(pages) <= 20:
        return SiteViewModel(site=site,
                             contents=random.choice(pages),
                             panels=[random.choice(pages) for x in range(6)],
                             page_list=pages)

    # 最新の10件からviewが多い1件を取る
    new_list = sorted(pages, key=lambda x: x.id, reverse=True)[:10]
    new_list = sorted(new_list, key=lambda x: x.view_count, reverse=True)
    contents = new_list[0]
    new_list = new_list[1:]
    pages_repository.pop(contents.id)

    # 人気順に並んだ最新の9件からパネル用の3件を取る
    random.shuffle(new_list)
    panels = new_list[1:4]
    for panel_page in panels:
        panel_page.set_favorite()
        pages_repository.pop(panel_page.id)

    # 残りの46件からviewが多い3件を取る
    left_pages = pages_repository.values()
    left_pages = sorted(left_pages, key=lambda x: x.view_count, reverse=True)
    for x in range(3):
        panels.append(left_pages.pop())
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


    return SiteViewModel(site=site,
                         contents=contents,
                         panels=panels,
                         page_list=left_pages)
