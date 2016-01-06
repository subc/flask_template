# -*- coding: utf-8 -*-


from module.scraping.subjects import Subject

ignore_base = [
    '晒',
    '叩',
    'フレンド',
    '協力',
    '交換',
    '終わった',
    '募集'
]


class SearchManager(object):
    """
    スレッドを検索する
    """
    def search(self, site):
        # スレッド検索
        subjects = Subject.get_from_url(site)
        method = getattr(self, site.title)
        subjects_dict = method(subjects, site)
        for key in subjects_dict:
            print(subjects_dict[key])

    def search_and_scraping(self, site, force=None):
        # スレッド検索
        subjects = Subject.get_from_url(site)
        method = getattr(self, site.title)
        subjects_dict = method(subjects, site)

        # スクレイピング
        for key in subjects_dict:
            sub = subjects_dict[key]
            sub.execute_matome(force=force)

        # 参照を切る
        method = None
        del method
        return subjects_dict

    def phantom(self, subjects, site):
        """
        ファンキル
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'ファンキル',
            'オブキル',
        ]
        keywords_ignore = ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def fallout4(self, subjects, site):
        """
        ファンキル
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'Fallout4',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def fallout4pc(self, *args, **kwargs):
        return self.fallout4(*args, **kwargs)

    def shironeko(self, subjects, site):
        """
        ファンキル
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            '白猫',
        ]
        keywords_ignore = [
            '糞猫',
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def logres(self, subjects, site):
        """
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'ログレス',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def pawaapp(self, subjects, site):
        """
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'パワプロ',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def pd(self, subjects, site):
        """
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'パズドラ',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def mstrike(self, subjects, site):
        """
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'モンスト',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def destiny(self, subjects, site):
        """
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'destiny',
            'Destiny',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def ffbe(self, subjects, site):
        """
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'FFBE',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def tos(self, subjects, site):
        keywords = [
            'Savior',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def dq10(self, subjects, site):
        keywords = [
            'DQ10',
            'DQX',
            'ドラゴンクエストX',
            'ドラゴンクエスト10',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def fgo(self, subjects, site):
        keywords = [
            'Grand Order',
            'FateGO',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def splatoon(self, subjects, site):
        keywords = [
            'Splatoon',
            'スプラトゥーン',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def star(self, subjects, site):
        keywords = [
            '星の',
            'スプラトゥーン',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def ffrk(self, subjects, site):
        keywords = [
            'FFRK',
        ]
        keywords_ignore = [
            '動画配信',
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def sekaiju(self, subjects, site):
        keywords = [
            '世界樹',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def lol(self, subjects, site):
        keywords = [
            'LoL',
            'League of Legends',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)


def _base_search(subjects, site, keywords, keywords_ignore):
    """
    :param subjects: list[Subject]
    :param site: Site
    :param keywords: list[str]
    :param keywords_ignore: list[str]
    :return: dict{id: Subject}
    """
    # 名前でフィルタ
    subjects_dict = {}
    for key in keywords:
        for subject in subjects:
            if key in subject.title:
                subjects_dict[subject.dat] = subject

    # 禁止名でフィルタ
    ignore_keys = []
    for key_subject in subjects_dict:
        _subject = subjects_dict[key_subject]
        _title = _subject.title
        for key_ignore in keywords_ignore:
            if key_ignore in _title:
                ignore_keys.append(key_subject)

    # 禁止名でフィルタの削除部分
    for key in ignore_keys:
        if key in subjects_dict:
            del subjects_dict[key]

    # 結果出力
    for key_subject in subjects_dict:
        print(subjects_dict[key_subject].title)

    return subjects_dict
