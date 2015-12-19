# -*- coding: utf-8 -*-
import datetime
from pip._vendor.distlib.util import cached_property
from sqlalchemy import Column, String, Integer, Text, UnicodeText, UniqueConstraint, Index, desc
from sqlalchemy.ext.declarative import declarative_base
from module.db.base import DBBaseMixin, CreateUpdateMixin
import enum

from module.site.keyword import Keyword
from module.site.site import Site
from utils.tls_property import cached_tls

Base = declarative_base()


class PageType(enum.Enum):
    # 投稿者の評価順
    POST_RANK = 1
    # キーワードとの一致度順
    KEYWORD_RANK = 2


class PageViewCountColor(enum.Enum):
    SUPERNOVA = 1
    HOT = 2


class Page(DBBaseMixin, CreateUpdateMixin, Base):
    site_id = Column('site_id', Integer, index=True)
    dat_id = Column('dat_id', Integer, index=True)
    page = Column('page', UnicodeText)
    view_count = Column('view_count', Integer, index=True, default=0)
    page_top = Column('page_top', UnicodeText)
    type = Column('type', Integer, index=True, default=0)  # PageTypeのenum
    _keywords = Column('_keywords', String(1000))

    def __repr__(self):
        return 'Page[{}]'.format(str(self.id))

    @classmethod
    @cached_tls
    def get(cls, pk):
        """
        :param pk: int
        :rtype: cls
        """
        return cls.objects().get(pk)

    @cached_property
    def site(self):
        return Site.get(self.site_id)

    @cached_property
    def background_image(self):
        image_id = self.site.get_background_image_id(self.id)
        return '/static/img/site/{}/{}.png'.format(self.site.title, image_id)

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
    def sub_time(self):
        """
        表示用
        """
        t = self.created_at + datetime.timedelta(hours=8)
        return t.strftime("%Y/%m/%d")

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

    def generate_top_body(self, _limit):
        top_body = self.page_top.replace('<br/>', '')
        if len(top_body) <= _limit + 3:
            return top_body
        return top_body[:_limit] + '...'

    def generate_top_title(self, _limit):
        top_body = self.page_top.replace('<br/>', '')
        if not self.is_post_rank and self.keyword_top:
            # キーワードとの親和度
            last = _limit - len(self.keyword_top.keyword)
            s = '【{}】{}'.format(self.keyword_top.keyword, top_body[:last])
            return s + '...'

        # 投稿者の評価順
        return top_body[:_limit] + '...'

    @cached_property
    def tile_body(self):
        return self.generate_top_body(60)

    @cached_property
    def list_label(self):
        return self.generate_top_title(35)

    @cached_property
    def tile_label(self):
        return self.generate_top_title(17)

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

    @property
    def view_text(self):
        # todo dummy 日本語表示 kとかMとか
        return self.view_count

    @classmethod
    def get_history(cls, site_id, pk_until, _limit=100):
        """
        特定id以下のrecordをN件取得
        :param site_id: int
        :param pk_until: int
        :param _limit: int
        :return:
        """
        return cls.objects().filter(cls.site_id==site_id,
                                    cls.id<=pk_until).order_by(desc(cls.id)).limit(_limit).all()

    @classmethod
    @cached_tls
    def get_new_history(cls, site_id, _limit=100):
        """
        最新のrecordをN件取得
        :param site_id: int
        :param _limit: int
        :return:
        """
        return cls.objects().filter(cls.site_id == site_id).order_by(desc(cls.id)).limit(_limit).all()

    def set_color_supernova(self):
        self.text_color = PageViewCountColor.SUPERNOVA.name

    def set_color_hot(self):
        self.text_color = PageViewCountColor.HOT.name

    def count_up(self):
        self.view_count += 1
        self.save()
