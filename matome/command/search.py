# -*- coding: utf-8 -*-
from flask_script import Command
from module.scraping.search import SearchManager
from module.site.site import Site


class Search(Command):
    """
    subject.txtを解析して、スレッド一覧をprintする
    """

    def run(self):
        self._run()

    def _run(self):
        for site in Site.get_all():
            print("-----------------")
            print(site.id, site.title)
            print("-----------------")
            SearchManager().search(site)
