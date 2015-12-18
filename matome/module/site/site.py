# -*- coding: utf-8 -*-
from pip._vendor.distlib.util import cached_property
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin, CreateUpdateMixin
from utils.tls_property import cached_tls

Base = declarative_base()


class Site(DBBaseMixin, CreateUpdateMixin, Base):
    name = Column('name', String(50))
    short_name = Column('short_name', String(20))
    title = Column('title', String(10), index=True)
    url = Column('url', String(200))
    background_image_count = Column('background_image_count', Integer)

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

    @cached_property
    def top_image_path(self):
        """
        /static/img/site/{title}/top.jpg
        :return:str
        """
        return '/static/img/site/{}/top.jpg'.format(self.title)

    @property
    def subjects_url(self):
        """
        http://anago.2ch.sc/applism/subject.txt
        :return:str
        """
        return '{}subject.txt'.format(self.url)

    def get_background_image_id(self, _id):
        return 1 + _id % self.background_image_count
