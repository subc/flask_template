# -*- coding: utf-8 -*-
import datetime

import pytz
from pip._vendor.distlib.util import cached_property
from sqlalchemy import Column, String, Integer, Text, UnicodeText, UniqueConstraint, Index, desc, DateTime
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


class PageViewLevel(enum.Enum):
    SUPERNOVA = 1
    HOT = 2
    WARM = 3
    NORMAL = 4


class Page(DBBaseMixin, CreateUpdateMixin, Base):
    site_id = Column('site_id', Integer, index=True)
    dat_id = Column('dat_id', Integer, index=True)
    page = Column('page', UnicodeText)
    view_count = Column('view_count', Integer, index=True, default=0)
    page_top = Column('page_top', UnicodeText)
    type = Column('type', Integer, index=True, default=0)  # PageTypeのenum
    _keywords = Column('_keywords', String(1000))
    start_at = Column(DateTime, default=None, nullable=True)

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

    @classmethod
    @cached_tls
    def get_by_site(cls, pk, site_id):
        """
        :param pk: int
        :param site_id: int
        :rtype: cls
        """
        return cls.objects().filter(cls.id==pk, cls.site_id==site_id).all()[0]

    @classmethod
    @cached_tls
    def get_prev(cls, pk, site_id):
        """
        1つ前のページを返却

        # 以下
        select * from page
        where id < 6500
        order by id desc
        limit 1
        >>6499

        :param pk: int
        :param site_id: int
        :rtype: cls
        """
        return cls.objects().filter(cls.id<pk, cls.site_id==site_id).order_by(desc(cls.id)).first()

    @cached_property
    def site(self):
        return Site.get(self.site_id)

    @cached_property
    def background_image(self):
        image_id = self.site.get_background_image_id(self.id)
        return '/static/img/site/{}/{}.jpg'.format(self.site.title, image_id)

    @property
    def is_post_rank(self):
        return self.type == PageType.POST_RANK.value

    @cached_property
    def time(self):
        """
        表示用
        """
        base_time = self.start_at if self.start_at else self.created_at
        t = base_time + datetime.timedelta(hours=8)
        return t.strftime("%Y年%m月%d日 %H:%M")

    @cached_property
    def sub_time(self):
        """
        表示用
        """
        base_time = self.start_at if self.start_at else self.created_at
        t = base_time + datetime.timedelta(hours=8)
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

    @cached_property
    def prev_page(self):
        """
        1つ前のページ
        :return: Page
        """
        return self.get_prev(self.id, self.site_id)

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
            if last < 0:
                last = 0

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
        if not words:
            return []

        # countが2以下のものは非表示
        words = [w for w in words if w.count > 2]
        if not words:
            return []

        # 並び替えて6個返却
        words = sorted(words, key=lambda x: x.id, reverse=True)
        words = sorted(words, key=lambda x: x.count, reverse=True)
        if words:
            return words[:6]
        return []

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
        if self.keywords:
            return self.keywords[0]
        return None

    @property
    def star_level(self):
        """
        0 - 50の範囲を返却

        /*星5.0: <div class="starlevel5 star50"></div>*/
        /*星4.0: <div class="starlevel5 star40"></div>*/
        /*星3.0: <div class="starlevel5 star30"></div>*/
        /*星2.0: <div class="starlevel5 star20"></div>*/
        /*星1.0: <div class="starlevel5 star10"></div>*/
        /*星0.0: <div class="starlevel5 star00"></div>*/

        /*星4.5: <div class="starlevel5 star45"></div>*/
        /*星3.5: <div class="starlevel5 star35"></div>*/
        /*星2.5: <div class="starlevel5 star25"></div>*/
        /*星1.5: <div class="starlevel5 star15"></div>*/
        /*星0.5: <div class="starlevel5 star05"></div>*/
        http://allabout.co.jp/gm/gc/24018/3/
        :return: int
        """
        if self._level is PageViewLevel.SUPERNOVA:
            return "starlevel5 star50"

        if self._level is PageViewLevel.HOT:
            return "starlevel5 star40"

        if self._level is PageViewLevel.WARM:
            return "starlevel5 star35"

        if self._level is PageViewLevel.NORMAL:
            return None

        return None

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

    @classmethod
    def get_feature_page(cls, site_id):
        """
        未来日に公開設定してあるページの件数を返却
        :param site_id: int
        :return: list(Page)
        """
        # 300件取る
        pages = cls.objects().filter(cls.site_id == site_id).order_by(desc(cls.id)).limit(300).all()

        if pages:
            now = datetime.datetime.now(pytz.utc)
            return [page for page in pages if not page.is_enable(now)]
        return []

    def get_history_from_myself(self):
        """
        自身のIDを基準にデータ取得
        :return: list(Page)
        """
        return Page.get_history(self.site_id, self.id - 1, _limit=20)

    def set_favorite(self, result):
        """
        :param result: bool
        """
        self.is_favorite = result

    def set_view_level(self, level):
        """
        :param level: PageViewLevel
        """
        self._level = level

    def count_up(self, count=1):
        self.view_count += count
        self.save()

    def is_enable(self, now):
        """
        有効ならTrue
        :param now: datetime
        :return: bool
        """
        if self.start_at is None:
            return True
        return pytz.utc.localize(self.start_at) < now
