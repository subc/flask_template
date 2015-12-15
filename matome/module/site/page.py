# -*- coding: utf-8 -*-
import datetime
from pip._vendor.distlib.util import cached_property
from sqlalchemy import Column, String, Integer, Text, UnicodeText, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin, CreateUpdateMixin

Base = declarative_base()


class Page(DBBaseMixin, CreateUpdateMixin, Base):
    site_id = Column('site_id', Integer, index=True)
    dat_id = Column('dat_id', Integer, index=True)
    page = Column('page', UnicodeText)
    view_count = Column('view_count', Integer, index=True, default=0)
    page_top = Column('page_top', UnicodeText)

    def __init__(self, site_id, dat_id, page):
        self.site_id = site_id,
        self.dat_id = dat_id
        self.page = page

    @cached_property
    def time(self):
        t = self.created_at + datetime.timedelta(hours=8)
        return t.strftime("%Y年%m月%d日 %H:%M")

    @cached_property
    def keywords(self):
        # todo
        return ['芭蕉扇', 'シェキナー', '剣斧槍ユニット']


class PageKeywordRelation(DBBaseMixin, Base):
    page_id = Column('page_id', Integer)
    keyword_id = Column('keyword_id', Integer)


class Keyword(DBBaseMixin, Base):
    site_id = Column('site_id', Integer)
    keyword = Column('keyword', String(255))
    count = Column('count', Integer)
