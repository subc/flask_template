# -*- coding: utf-8 -*-
from flask_script import Command

from module.site.page import Page
from module.site.page_keyword import PageKeywordRelation


class CreatePageKeywordRelation(Command):
    """
    PageKeywordRelationを再生成する
    """
    def run(self):
        # PageKeywordRelationに1行でもレコードあれば実行しない
        if PageKeywordRelation.objects().filter().count() > 0:
            raise AssertionError("PageKeywordRelation data is exist")

        # pageとkeywordのデータ全取得
        page_all = Page.get_all()
        page_all = sorted(page_all, key=lambda x: x.id)

        # 10ページずつbulk
        count = 0
        pages = []
        for page in page_all:
            pages.append(page)
            count += 1
            if len(pages) > 10:
                PageKeywordRelation.register(pages)
                pages = []
                print("{}/{}".format(count, len(page_all)))
        PageKeywordRelation.register(pages)
