# -*- coding: utf-8 -*-
import redis


EXPIRE = 3600 * 24 * 30  # 30日
KEY = 'SCRAPING:{}:{}'


class SearchStorage(object):
    """
    redisで検索履歴を管理
    """
    _cli = None

    def __init__(self, site_name):
        self.site_name = site_name

    @property
    def client(self):
        if not self._cli:
            host = self.config.get('REDIS').get('default').get('host')
            port = self.config.get('REDIS').get('default').get('port')
            db = self.config.get('REDIS').get('default').get('db')
            self._cli = redis.Redis(host=host, port=port, db=db)
        return self._cli

    @property
    def config(self):
        from app import conf
        return conf()

    def get_key(self, dat):
        return KEY.format(self.site_name, dat)

    def set_dat(self, dat):
        self.client.set(self.get_key(dat), 1)
        self.touch(self.get_key(dat))

    def get_dat(self, dat):
        return self.client.get(self.get_key(dat))

    def touch(self, key, expire=EXPIRE):
        self.client.expire(key, expire)
