# -*- coding: utf-8 -*-
from collections import defaultdict

from flask import Blueprint, redirect, request
import redis
from uuid import uuid4


app = Blueprint("vote",
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは {{ url_for('sitemap.sitemap') }}
@app.route("/", methods=['POST'])
def vote():
    """
    vote

    >> request.form
    ImmutableMultiDict([('check', '305'), ('check', '215'), ('check', '180'), ('name', 'qq')])
    """
    error = None
    redirect_url = "http://subc.github.io/vote/result.html"
    user_name = None
    vote_ids = []
    print(request.form)
    for key in request.form.keys():
        print(key, request.form.get(key))
        v = request.form.get(key)
        if 'check' in key:
            vote_ids.append(int(v))
        if key == 'name':
            user_name = v

    # すでに登録済みです。
    if not VoteStorage.can_vote(user_name):
        error = '既に登録済みです。'

    # 記事推薦数が6件以上です。
    print(vote_ids)
    if len(vote_ids) > 5:
        error = '記事推薦数が6件以上です。'

    # 3件未満
    if len(vote_ids) < 3:
        error = '記事推薦数が3件未満です。'

    # お名前が未入力です。
    if not user_name:
        error = 'お名前が未入力です'

    if error:
        return redirect("{}?q=ERROR:{}".format(redirect_url, error), code=302)

    # 登録
    VoteStorage.set(user_name, vote_ids)

    return redirect("{}?q=投票ありがとうございます。".format(redirect_url), code=302)


@app.route("/result/", methods=['GET'])
def result():
    r = VoteStorage.get_result().items()
    r = sorted(r, key=lambda x: x[1], reverse=True)
    body = ''
    for k, v in r:
        body += '{}:{}<br />'.format(k, v)
    return body


@app.route("/delete123/", methods=['GET'])
def delete():
    VoteStorage.delete_all()
    return 'delete 成功'


class VoteStorage(object):
    BASE_KEY = 'VOTE:RESULT:{}:'
    _cli = None

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

    @classmethod
    def can_vote(cls, user_name):
        return user_name not in cls.get_names()

    @classmethod
    def get_names(cls):
        storage = VoteStorage()
        names = []
        for key in cls.get_keys():
            names.append(storage.client.hget(key, 'name'))
        return [n.decode("utf-8") for n in names]

    @classmethod
    def set(cls, user_name, vote_ids):
        key = cls.get_key(str(uuid4()))
        param = {
            'name': user_name,
            'vote_ids': ','.join([str(pk) for pk in vote_ids]),
        }

        # hash書き込み
        storage = VoteStorage()
        storage.client.hmset(key, param)

    @classmethod
    def get_result(cls):
        """
        記事id: 投稿数
        :return: dict[int: int]
        """
        storage = VoteStorage()
        r = defaultdict(int)
        for key in cls.get_keys():
            vote_ids = storage.client.hget(key, 'vote_ids')
            print(vote_ids)
            vote_ids = vote_ids.decode("utf-8")

            # try:
            for pk in [int(pk) for pk in vote_ids.split(',')]:
                print(pk)
                r[pk] += 1
            # except:
            #     pass
        return r

    @classmethod
    def get_keys(cls):
        storage = VoteStorage()
        key = cls.get_key('*')
        return storage.client.keys(key)

    @classmethod
    def get_key(cls, token):
        return cls.BASE_KEY.format(token)

    @classmethod
    def delete_all(cls):
        storage = VoteStorage()
        for key in cls.get_keys():
            storage.client.delete(key)
