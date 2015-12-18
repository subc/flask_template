# -*- coding: utf-8 -*-
from flask_script import Command, Option

from command.insert_inspecton import INSPECTION_WORD
from module.scraping.inspection import InspectionWord
from module.scraping.search import SearchManager
from module.site.site import Site


class Scraping(Command):
    """
    Siteデータを元にスクレイピングする
    """
    option_list = (
        Option('-f', '--force', default=None, required=False, help='ignore redis scraping history'),
    )

    def run(self, force=None):
        self.init()
        self._run(force)

    def init(self):
        # NGワードを再読み込み
        InspectionWord.register(INSPECTION_WORD)

    def _run(self, force=None):
        site = Site.get(1)
        SearchManager().search_and_scraping(site, force=force)

        site = Site.get(2)
        SearchManager().search_and_scraping(site, force=force)
