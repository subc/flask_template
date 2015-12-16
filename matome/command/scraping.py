# -*- coding: utf-8 -*-
from flask_script import Command
from module.scraping.search import SearchManager
from module.site.site import Site


class Scraping(Command):
    """
    Siteデータを元にスクレイピングする
    """

    def run(self):
        print("start")
        self._run()
        print("finish")

    def _run(self):
        site = Site.get(1)
        SearchManager().search_and_scraping(site)
