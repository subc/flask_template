# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin
import datetime

Base = declarative_base()


class Site(DBBaseMixin, Base):
    name = Column('title', String(10))
    url = Column('url', String(200))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, nullable=True)

    def __init__(self, name, url):
        self.name = name
        self.url = url
