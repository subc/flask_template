# -*- coding: utf-8 -*-
import re
import traceback

import time
from collections import defaultdict

import requests
from flask_script import Command, Option
from janome.tokenizer import Tokenizer

from command.insert_inspection import INSPECTION_WORD
from module.scraping.inspection import InspectionWord
from module.scraping.search import SearchManager
from module.scraping.subjects import Subject
from module.site.site import Site


class Pickup(Command):
    """
    Siteデータを元に記事をピックアップする
    """
    option_list = (
        Option('-f', '--force', default=None, required=False, help='ignore redis scraping history'),
    )

    def run(self, force=None):
        print('start')
        # 全サイト取得と重複排除
        sites = {}
        for site in Site.get_all():
            sites[site.url] = site

        # リストに対してignoreとkeywordマッチを排除
        sure = []
        for key in sites:
            site = sites[key]
            response = requests.get(site.subjects_url)
            assert (response.status_code == 200), response.text

            # parse
            data = list(response.text.split('\n'))
            for line in data:
                try:
                    _ = Subject(site, line)
                    sure.append(_)
                except:
                    pass

        print(sure)

        # リスト出力
        t = Tokenizer()
        r = defaultdict(int)
        r2 = defaultdict(list)
        r3 = defaultdict(int)
        for _sure in sure:
            try:
                for token in t.tokenize(_sure.title):
                    if not token_filter(token):
                        r[token.surface] += 1
                        r2[token.surface] += [_sure]
                        r3[token] += 0
            except:
                pass

        # sort
        sure = sorted(sure, key=lambda x: x.title)

        for _sure in sure:
            try:
                point = 0
                for token in t.tokenize(_sure.title):
                    if not token_filter(token):
                        point += r[token.surface]
                if not filter_title(point, _sure):
                    print(_sure.title, _sure.count_res)

            except:
                pass


        # r4 = defaultdict(int)
        # for _t in r3:
        #     # print(_t.surface, r[_t.surface], ':'.join([_.title for _ in r2[_t.surface]]))
        #     # print(_t.surface, r[_t.surface])
        #     __sure = r2[_t.surface]
        #     r4[__sure.title] += r[_t.surface]
        #
        # # print
        # for key in r4:
        #     print(key, r4[key])


def token_filter(token):
    if "動詞" in token.part_of_speech:
        return True

    if "助" in token.part_of_speech:
        return True

    if "記号" in token.part_of_speech:
        return True

    if "数" in token.part_of_speech:
        return True

    if "サ変接続" in token.part_of_speech:
        return True

    # 英語をキーワードに含めない（offにするとURLをまとめはじめる）
    if re.match(r'[a-zA-Z0-9]', token.surface):
        return True
    return False


def filter_title(point, sure):
    title = sure.title

    if sure.count_res <= 200:
        return True

    if point <= 0:
        return True

    ignore = [
        'ドラクエ', 'ドラゴン', 'DQ10', 'ドラゴンクエストX',
        '星ドラ',
        'DQMSL',
        'ダークソウル', 'DARK SOULS', 'Bloodborne',
        'LoL', 'lol',
        '白猫',
        '黒猫',
        '世界樹',
        'FFBE',
        'モンスト',
        'Splatoon',
        'Fate/Grand', 'FGO', 'FateGO',
    ]

    for kw in ignore:
        if kw in title:
            return True
    return False
