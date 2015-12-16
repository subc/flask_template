# -*- coding: utf-8 -*-
import re

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin

Base = declarative_base()


class InspectionWord(DBBaseMixin, Base):
    word = Column('word', String(30), unique=True)

    # クラスオブジェクトにキャッシュ
    _INSPECTION_PATTERN = None

    @classmethod
    def register(cls, keywords):
        """
        NG Wordを登録
        :param keywords: lost[str]
        """
        # 重複排除
        all_record = cls.get_all()
        d = {record.word: record for record in all_record}

        objs = [cls(word=k) for k in keywords if k not in d]
        InspectionWord.bulk_insert(objs)

    @classmethod
    def get_all(cls):
        return cls.objects().all()

    @classmethod
    def get_re_compile(cls):
        """
        禁止文字にマッチさせるための正規表現文字列
        :rtype : _sre.SRE_Pattern
        """
        if cls._INSPECTION_PATTERN:
            return cls._INSPECTION_PATTERN
        body = '|'.join([record.word for record in cls.get_all()])
        r = re.compile("({})".format(body))
        cls._INSPECTION_PATTERN = r
        return r

    @classmethod
    def inspection(cls, word):
        """
        ワードが禁止文字列を含んでいるとTrue
        :param word: unicode
        :rtype : bool
        """
        if len(word.strip()) == 0:  # 空白のみで構成されている
            return True
        r = cls.get_re_compile()
        m = r.search(word)
        return bool(m)
