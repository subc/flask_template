# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import random

from views.vote import VoteStorage
from uuid import uuid4


def test_storage():
    storage = VoteStorage()
    assert str == type(VoteStorage.get_key('hoge'))

    # 削除
    VoteStorage.delete_all()

    # 登録
    user_name = 'hami'
    vote_ids = [1, 3, 6, 10]
    VoteStorage.set(user_name, vote_ids)

    # 一覧
    assert VoteStorage.get_keys()

    # 登録ユーザ名一覧
    assert VoteStorage.get_names()

    # 登録可能か
    assert VoteStorage.can_vote(user_name) is False
    assert VoteStorage.can_vote(user_name + '2') is True

    # 複数登録
    for x in range(100):
        VoteStorage.set(user_name + str(random.randint(1000, 1000000)),
                        [random.randint(1, 100),
                         random.randint(1, 100),
                         random.randint(1, 100),
                         random.randint(1, 100)])

    # 結果表示
    print(VoteStorage.get_result())
