# -*- coding: utf-8 -*-
import re

import requests
from pip._vendor.distlib.util import cached_property

from app import conf
from module.scraping.matome import MatomeMixin
from module.scraping.storage import SearchStorage


class Subject(MatomeMixin):
    def __init__(self, site, line):
        self.site = site
        self._line = line

        # self check
        self.check(line)

    def __repr__(self):
        return 'Title:{} R:{} D:{}'.format(self.title, self.count_res, self.dat)

    @cached_property
    def dat(self):
        return self._line.split('<>')[0]

    @property
    def dat_id(self):
        return self.dat.replace('.dat', '')

    @cached_property
    def title(self):
        body = self._line.split('<>')[1]
        return body.replace('(' + str(self.count_res) + ')', '')

    @cached_property
    def count_res(self):
        body = self._line.split('<>')[1]
        tail6 = body[-6:]
        match_str = re.search(r'\(\d{1,4}\)', tail6).group(0)
        return int(match_str.replace('(', '').replace(')', ''))

    @cached_property
    def dat_url(self):
        """
        http://news22.2ch.net/newsplus/dat/1185716060.dat
        :return:
        """
        return '{}dat/{}'.format(self.site.url, self.dat)

    @property
    def storage(self):
        return SearchStorage(self.site.title)

    @classmethod
    def get_from_url(cls, site):
        """
        urlからダウンロードする
        :param site: Site
        :return: list[cls]
        """
        response = requests.get(site.subjects_url)
        assert (response.status_code == 200), response.text

        # parse
        data = list(response.text.split('\n'))

        # generate Subject
        r = []
        for line in data:
            try:
                _ = cls(site, line)
                r.append(_)
            except:
                pass

        # 投稿数でsubjectをフィルタリング
        limit = conf().get('SCRAPING_LIMIT')
        return [_r for _r in r if _r.count_res >= limit]

    def check(self, line):
        """
        正常なデータであること
        input example) 1449279464.dat<>白猫プロジェクト無課金スレ★1217 (827)
        :param line: s
        """
        assert len(line.split('<>')) == 2, line
        assert self.dat
        assert self.count_res
        assert self.title

    def is_enable(self):
        """
        まとめ可能ならTrue
        redisに問い合わせてチェック済みならFalse
        :return: bool
        """
        # 既にまとめ済みならスキップ
        already_matome = bool(self.storage.get_dat(self.dat_id))
        if already_matome:
            return False

        # レス数が900以上ならまとめる
        if self.count_res >= 900:
            return True
        else:
            return False

    def done(self):
        """
        まとめ終わったら再実行しないようにredisにフラグ立てる
        """
        self.storage.set_dat(self.dat_id)

    def execute_matome(self, force=None):
        """
        まとめる
        :param force: bool
        """
        Subject.matome(self, force=force)
