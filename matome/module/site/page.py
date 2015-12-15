# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin, CreateUpdateMixin

Base = declarative_base()


class Page(DBBaseMixin, CreateUpdateMixin, Base):
    site_id = Column('site_id', Integer)
    dat_id = Column('dat_id', Integer)
    page = Column('page', Text)

    def __init__(self, site_id, dat_id, page):
        self.site_id = site_id,
        self.dat_id = dat_id
        self.page = page


class PageKeywordRelation(DBBaseMixin, Base):
    page_id = Column('page_id', Integer)
    keyword_id = Column('keyword_id', Integer)


class Keyword(DBBaseMixin, Base):
    site_id = Column('site_id', Integer)
    keyword = Column('keyword', String(255))
    count = Column('count', Integer)
