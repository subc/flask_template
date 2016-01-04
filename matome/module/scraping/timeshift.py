# -*- coding: utf-8 -*-
import random
import pytz
import datetime

from module.site.page import Page


def set_start_at(pages):
        """
        48時間の値を最適化して設定する
        :param pages: list(Page)
        :return:
        """
        # 3件以下なら何もしない
        if len(pages) <= 3:
            return

        # 既に48時間先に10件以上予約がある場合は設定しない。
        feature_page = Page.get_feature_page(pages[0].site_id)
        print(feature_page)
        if len(feature_page) >= 10:
            return

        # 最適化して並び替える
        _today_page = pages[2:]
        _tomorrow_page = pages[:2]

        _set_start_at(_today_page)
        _set_start_at(_tomorrow_page, time_shift=datetime.timedelta(hours=24))


def _set_start_at(pages, time_shift=None):
    """
    start_at に未来日を設定する
    :param pages: list(Page)
    :param time_shift: datetime.timedelta
    """
    # 現在時間
    now = datetime.datetime.now(tz=pytz.utc)

    # 補正値
    count = 1

    for page in pages:
        page.start_at = get_time_shift(now, count, time_shift=time_shift)
        page.save()
        count += 1


def get_time_shift(now, count, time_shift=None):
    """
    現在時間からランダムで時間をずらす
    :param now:
    :param count:
    :param time_shift:
    :return:
    """
    base_sec = random.randint(3000, 4200)
    base_shift = datetime.timedelta(seconds=base_sec * count)
    if time_shift:
        return now + base_shift + time_shift
    return now + base_shift
