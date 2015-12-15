# -*- coding: utf-8 -*-
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin, CreateUpdateMixin

Base = declarative_base()


class Site(DBBaseMixin, CreateUpdateMixin, Base):
    name = Column('name', String(50))
    title = Column('title', String(10))
    url = Column('url', String(200))

    @property
    def subjects_url(self):
        """
        http://anago.2ch.sc/applism/subject.txt
        :return:str
        """
        return '{}subject.txt'.format(self.url)
