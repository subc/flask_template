# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin

Base = declarative_base()


class Book(DBBaseMixin, Base):
    title = Column('title', String(200))
    price = Column('price', Integer)
    publish = Column('publish', String(200))
    published = Column('published', String(200))

    def __init__(self, title, price, publish, published):
        self.title = title
        self.price = price
        self.publish = publish
        self.published = published
