# -*- coding: utf-8 -*-
import re

import requests
from pip._vendor.distlib.util import cached_property


class Subject(object):
    def __init__(self, line):
        # self check
        Subject.check(line)

        self._line = line
        self.dat
        self.count_res
        self.title

    def __repr__(self):
        return 'Title:{} R:{} D:{}'.format(self.title, self.count_res, self.dat)

    @cached_property
    def dat(self):
        return self._line.split('<>')[0]

    @cached_property
    def title(self):
        body = self._line.split('<>')[1]
        return body.replace('(' + str(self.count_res) + ')', '')

    @cached_property
    def count_res(self):
        body = self._line.split('<>')[1]
        tail6 = body[-6:]
        match_str = re.search(r'\(\d{1,4}\)', tail6).group(0)
        return match_str.replace('(', '').replace(')', '')

    @classmethod
    def get_from_url(cls, url):
        """
        urlからダウンロードする
        :param url: str
        :return: list[cls]
        """
        response = requests.get(url)
        assert (response.status_code == 200), response.text

        # parse
        data = list(response.text.split('\n'))

        # generate Subject
        r = []
        for line in data:
            try:
                _ = cls(line)
                r.append(_)
            except:
                pass
        print(r)
        return r

    @classmethod
    def check(cls, line):
        """
        正常なデータであること
        input example) 1449279464.dat<>白猫プロジェクト無課金スレ★1217 (827)
        :param line: s
        """
        assert len(line.split('<>')) == 2, line

    def printer(self):
        print(self)
