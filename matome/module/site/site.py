# -*- coding: utf-8 -*-
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin, CreateUpdateMixin
from utils.tls_property import cached_tls

Base = declarative_base()


class Site(DBBaseMixin, CreateUpdateMixin, Base):
    name = Column('name', String(50))
    title = Column('title', String(10), index=True)
    url = Column('url', String(200))

    @classmethod
    @cached_tls
    def get(cls, pk):
        """
        :param pk: int
        :rtype: cls
        """
        return cls.objects().get(pk)

    @classmethod
    @cached_tls
    def get_title(cls, title):
        """
        :param title: int
        :rtype: cls
        """
        return cls.objects().filter(cls.title==title)[0]

    @property
    def subjects_url(self):
        """
        http://anago.2ch.sc/applism/subject.txt
        :return:str
        """
        return '{}subject.txt'.format(self.url)
