# -*- coding: utf-8 -*-
import datetime
from pip._vendor.distlib.util import cached_property
from sqlalchemy import Column, String, Integer, Text, UnicodeText, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin, CreateUpdateMixin
import enum

Base = declarative_base()


class PageType(enum.Enum):
    # 投稿者の評価順
    POST_RANK = 1
    # キーワードとの一致度順
    KEYWORD_RANK = 2


class Page(DBBaseMixin, CreateUpdateMixin, Base):
    site_id = Column('site_id', Integer, index=True)
    dat_id = Column('dat_id', Integer, index=True)
    page = Column('page', UnicodeText)
    view_count = Column('view_count', Integer, index=True, default=0)
    page_top = Column('page_top', UnicodeText)
    type = Column('type', Integer, index=True, default=0)  # 1.. post rank 2.. keyword

    @property
    def is_post_rank(self):
        return self.type == PageType.POST_RANK.value

    @cached_property
    def time(self):
        """
        表示用
        """
        t = self.created_at + datetime.timedelta(hours=8)
        return t.strftime("%Y年%m月%d日 %H:%M")

    @cached_property
    def tile_body(self):
        _limit = 60
        if len(self.page_top) <= _limit + 3:
            return self.page_top
        return self.page_top[:60] + '...'

    @cached_property
    def tile_label(self):
        _limit = 17
        if not self.is_post_rank and self.keyword_top:
            # キーワードとの親和度
            last = _limit - len(self.keyword_top)
            s = '【{}】{}'.format(self.keyword_top, self.page_top[:last])
            return s + '...'

        # 投稿者の評価順
        return self.page_top[:_limit] + '...'

    @cached_property
    def keywords(self):
        # todo
        return ['芭蕉扇', 'シェキナー', '剣斧槍ユニット']

    @property
    def keyword_top(self):
        if self.keywords:
            return self.keywords[0]
        return None


class PageKeywordRelation(DBBaseMixin, Base):
    page_id = Column('page_id', Integer)
    keyword_id = Column('keyword_id', Integer)


class Keyword(DBBaseMixin, Base):
    site_id = Column('site_id', Integer)
    keyword = Column('keyword', String(255))
    count = Column('count', Integer)
