# -*- coding: utf-8 -*-
from flask_script import Command, Option
from flask import Flask, request, current_app
from app import create_app
import config.production
import json
from requests_oauthlib import OAuth1Session
import re
import collections

class TaskTwitter(Command):
    """
    てすと
    """
    option_list = (
        Option('-k', '--keyword', default=None, required=True, help='search keyword'),
    )

    def run(self, keyword=None):
        print("start")
        self.init()
        self._run(keyword)
        print("finish")

    def init(self):
        pass

    @property
    def app(self):
        return create_app(config.production)

    def _run(self, keyword):
        print("keyword:{key}".format(key=keyword))
        self.search(keyword)

    @staticmethod
    def katakana(d, s):
        re_katakana = re.compile(r'[\u30A1-\u30F4]+')
        result_all = re_katakana.findall(s)
        for r in result_all:
            if len(r) < 3:
                continue
            d[r] += 1

    def search(self, keyword):
        tw = self.app.config['TWITTER']
        params = {'q' : keyword, 'count' : 100, 'lang': 'ja'}
        twitter = OAuth1Session(tw.CONSUMER_KEY, tw.CONSUMER_SECRET, tw.ACCESS_TOKEN, tw.ACCESS_TOKEN_SECRET)
        url = "https://api.twitter.com/1.1/search/tweets.json"
        req = twitter.get(url, params = params)
        d = collections.defaultdict(int)

        if req.status_code == 200:
            search_timeline = json.loads(req.text)
            for tweet in search_timeline['statuses']:
                self.katakana(d, tweet['text'])
                print(tweet['user']['name'] + '::' + tweet['text'])
                print(tweet['created_at'])
                print('----------------------------------------------------')
        else:
            print("ERROR: %d" % req.status_code)
        return {k: v for k, v in d.items() if v > 1}
