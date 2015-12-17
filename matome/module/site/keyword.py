# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin
from utils.tls_property import cached_tls

Base = declarative_base()


class Keyword(DBBaseMixin, Base):
    site_id = Column('site_id', Integer, index=True)
    keyword = Column('keyword', String(255), index=True)
    count = Column('count', Integer, default=0)

    def __repr__(self):
        return '{0}[{1}]'.format(self.__class__.__name__, self.id)

    @classmethod
    @cached_tls
    def get(cls, pk):
        """
        :param pk: int
        :rtype: cls
        """
        return cls.objects().get(pk)

    @classmethod
    def get_by_keywords(cls, site_id, keywords):
        """
        :param site_id: int
        :param keywords: list(str)
        :return: list[Keyword]
        """
        return cls.objects().filter(cls.site_id==site_id, cls.keyword.in_(keywords)).all()

    @classmethod
    def register(cls, site_id, keywords):
        """
        keywordを一括登録する
        :param site_id: int
        :param keywords: list(str)
        :rtype : list[Keyword]
        """
        # 重複排除
        keywords = list(set(keywords))

        # 存在チェック
        keyword_records = cls.get_by_keywords(site_id, keywords)
        keyword_record_dict = {record.keyword: record for record in keyword_records}

        create_objs = []
        for keyword_str in keywords:
            if keyword_str in keyword_record_dict:
                # 存在するからカウントアップだけする
                keyword_record_dict[keyword_str].count_up()
            else:
                obj = cls(site_id=site_id, keyword=keyword_str, count=1)
                create_objs.append(obj)

        # バルク!
        objs = cls.bulk_insert(create_objs)

        return objs + keyword_records

    def count_up(self):
        self.count += 1
        self.save()
