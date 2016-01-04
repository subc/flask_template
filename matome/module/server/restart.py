# -*- coding: utf-8 -*-
from pip._vendor.distlib.util import cached_property
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin, CreateUpdateMixin
from utils.tls_property import cached_tls
import enum

Base = declarative_base()


class RestartCause(enum.Enum):
    UpdateContents = 1


class Restart(DBBaseMixin, CreateUpdateMixin, Base):
    site_id = Column('site_id', Integer)
    RestartCause = Column('cause', Integer)
    is_finish = Column('site_id', Boolean, index=True)

    @classmethod
    def get_new(cls):
        pass

    def register(self):
        pass

    def finish(self):
        """
        is_finish
        """
        pass
