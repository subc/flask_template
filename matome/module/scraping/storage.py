# -*- coding: utf-8 -*-
import redis


EXPIRE = 3600 * 24 * 30  # 30日


class SearchStorage(object):
    """
    redisで検索履歴を管理
    """
    _cli = None

    def __init__(self):
        pass

    @property
    def client(self):
        if self._cli:
            host = self.config.get('default').get('host')
            port = self.config.get('default').get('port')
            db = self.config.get('default').get('db')
            self._cli = redis.Redis(host=host, port=port, db=db)
        return self._cli

    @property
    def config(self):
        from app import create_app
        app = create_app()
        return app.config

    def touch(self, key, expire=EXPIRE):
            self.client.expire(key, expire)
