# -*- coding: utf-8 -*-
import traceback

import time
from flask_script import Command, Option

from command.insert_inspection import INSPECTION_WORD
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
        # supervisordでの連続実行エラー対策
        print("finish")
        print("supervisordでの連続実行エラー対策でスリープ開始")
        time.sleep(20)

    def init(self):
        # NGワードを再読み込み
        InspectionWord.register(INSPECTION_WORD)

    def _run(self, force=None):
        for site in Site.get_all():
            print(site)
            try:
                SearchManager().search_and_scraping(site, force=force)
            except AttributeError as err:
                traceback.print_tb(err.__traceback__)
                for x in range(100):
                    print('未設定エラー:{}:{}の検出関数が未設定'.format(site.id, site.title))
                break
            except Exception as err:
                traceback.print_tb(err.__traceback__)
