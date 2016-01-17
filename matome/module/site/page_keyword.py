# -*- coding: utf-8 -*-
import datetime

import pytz
from pip._vendor.distlib.util import cached_property
from sqlalchemy import Column, String, Integer, Text, UnicodeText, UniqueConstraint, Index, desc, func, or_
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin, CreateUpdateMixin
from module.site.page import Page
from utils.tls_property import cached_tls

Base = declarative_base()


class PageKeywordRelation(DBBaseMixin, Base):
    """
    キーワードに紐づくページを取得するため
    """
    page_id = Column('page_id', Integer)
    keyword_id = Column('keyword_id', Integer, index=True)

    @classmethod
    @cached_tls
    def get_from_new_keyword(cls, keyword_id, _limit=100):
        return cls.objects().filter(cls.keyword_id==keyword_id).order_by(desc(cls.id)).limit(_limit).all()

    @classmethod
    def get_from_keyword(cls, keyword_id, pk_until, _limit=100):
        """
        :param keyword_id: int
        :param pk_until: int
        :param _limit:
        :return: list(cls)
        """
        return cls.objects().filter(cls.keyword_id==keyword_id, cls.id<=pk_until).order_by(desc(cls.id)).limit(_limit).all()

    @classmethod
    @cached_tls
    def get_count(cls, keyword_id):
        return cls.objects().filter(cls.keyword_id==keyword_id).count()

    @cached_property
    def page(self):
        return Page.get(self.page_id)

    @classmethod
    def gets_new(cls, _limit):
        return cls.objects().filter().order_by(desc(cls.id)).limit(_limit).all()

    @classmethod
    def register(cls, pages):
        """
        pagesデータからレコードを一括生成する
        :param pages: list[Page]
        """
        objs = []
        for page in pages:
            for keyword in page.keywords:
                obj = cls(page_id=page.id, keyword_id=keyword.id)
                objs.append(obj)

        # バルク!
        cls.bulk_insert(objs)
