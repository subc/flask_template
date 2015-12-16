# -*- coding: utf-8 -*-
import datetime
from pip._vendor.distlib.util import cached_property
from sqlalchemy import Column, String, Integer, Text, UnicodeText, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin, CreateUpdateMixin
import enum

from utils.tls_property import cached_tls

Base = declarative_base()


class PageType(enum.Enum):
    # 投稿者の評価順
    POST_RANK = 1
    # キーワードとの一致度順
    KEYWORD_RANK = 2


class Page(DBBaseMixin, CreateUpdateMixin, Base):
    site_id = Column('site_id', Integer, index=True)
    dat_id = Column('dat_id', Integer, index=True)
    page = Column('page', UnicodeText)
    view_count = Column('view_count', Integer, index=True, default=0)
    page_top = Column('page_top', UnicodeText)
    type = Column('type', Integer, index=True, default=0)  # PageTypeのenum
    _keywords = Column('_keywords', String(1000))

    @property
    def is_post_rank(self):
        return self.type == PageType.POST_RANK.value

    @cached_property
    def time(self):
        """
        表示用
        """
        t = self.created_at + datetime.timedelta(hours=8)
        return t.strftime("%Y年%m月%d日 %H:%M")

    @cached_property
    def title(self):
        prefix = ''
        if not self.is_post_rank and self.keyword_top:
            # キーワードとの親和度
            prefix = '【{}】'.format(self.keyword_top.keyword)
        return prefix + self._top_first_line

    @cached_property
    def _top_first_line(self):
        """
        表示用: 最初の投稿者の1行目
        :return: str
        """
        if '<br/>' not in self.page_top:
            return self.page_top
        s = self.page_top.split('<br/>')
        return s[0]

    @cached_property
    def tile_body(self):
        _limit = 60
        top_body = self.page_top.replace('<br/>', '')
        if len(top_body) <= _limit + 3:
            return top_body
        return top_body[:60] + '...'

    @cached_property
    def tile_label(self):
        _limit = 17
        if not self.is_post_rank and self.keyword_top:
            # キーワードとの親和度
            last = _limit - len(self.keyword_top.keyword)
            s = '【{}】{}'.format(self.keyword_top.keyword, self.page_top[:last])
            return s + '...'

        # 投稿者の評価順
        return self.page_top[:_limit] + '...'

    @cached_property
    def keywords(self):
        """
        :return: list(Keyword)
        """
        words = [Keyword.get(_id) for _id in self._keyword_ids]
        words = sorted(words, key=lambda x: x.id, reverse=True)
        words = sorted(words, key=lambda x: x.count, reverse=True)
        return words

    @cached_property
    def _keyword_ids(self):
        """
        :return: list(int)
        """
        if not self._keywords:
            return []
        if ',' not in self._keywords:
            return [int(self._keywords)]
        return [int(_id) for _id in self._keywords.split(',')]

    @property
    def keyword_top(self):
        if self._keywords:
            return self.keywords[0]
        return None

    def count_up(self):
        self.view_count += 1
        self.save()


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
