# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
import re
from utils.db import get_db_session
import datetime

Base = declarative_base()


def camel_to_snake(s):
    """
    >>> convert('CamelCase')
    'camel_case'
    >>> convert('CamelCamelCase')
    'camel_camel_case'
    >>> convert('Camel2Camel2Case')
    'camel2_camel2_case'
    >>> convert('getHTTPResponseCode')
    'get_http_response_code'
    >>> convert('get2HTTPResponseCode')
    'get2_http_response_code'
    >>> convert('HTTPResponseCode')
    'http_response_code'
    >>> convert('HTTPResponseCodeXYZ')
    'http_response_code_xyz'
    :param s: str
    :return: str
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class DBBaseMixin(object):
    id = Column('id', Integer, primary_key=True, index=True)

    def __repr__(self):
        return '<{0}.{1} object at {2}>'.format(
            self.__module__, type(self).__name__, hex(id(self)))

    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)

    @classmethod
    def objects(cls):
        """
        :rtype : sqlalchemy.orm.query.Query
        """
        return get_db_session().query(cls)

    @classmethod
    def session(cls):
        return get_db_session()

    @classmethod
    def get(cls, pk):
        """
        :param pk: int
        :rtype: cls
        """
        return cls.objects().get(pk)

    @classmethod
    def get_all(cls):
        return cls.objects().filter().all()

    @classmethod
    def insert(cls, obj):
        """
        :param obj: cls
        :rtype: cls
        """
        cls.session().add(obj)
        cls.session().commit()
        return obj

    @classmethod
    def bulk_insert(cls, objs):
        """
        :param objs: list[cls]
        :rtype: list[cls]
        """
        cls.session().add_all(objs)
        cls.session().commit()
        return objs

    def delete(self):
        session = self.__class__.session()
        session.query(self.__class__).filter(self.__class__.id==self.id).delete()
        session.commit()

    def save(self):
        """
        :return:self
        """
        session = self.__class__.session()
        try:
            session.add(self)
            session.commit()
        except sqlalchemy.exc.StatementError:
            session.rollback()
        return self


class CreateUpdateMixin(object):
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, nullable=True)
