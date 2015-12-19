# -*- coding: utf-8 -*-


from module.scraping.subjects import Subject


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
            'トムオ'
        ]
        keywords_ignore = [

        ]

        # 名前でフィルタ
        subjects_dict = {}
        for key in keywords:
            for subject in subjects:
                if key in subject.title:
                    subjects_dict[subject.dat] = subject

        # 禁止名でフィルタ

        return subjects_dict

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
            '晒',
            '叩'
        ]

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
            del subjects_dict[key]

        # 結果出力
        for key_subject in subjects_dict:
            print(subjects_dict[key_subject].title)

        return subjects_dict

    def fallout4pc(self, *args, **kwargs):
        return self.fallout4(*args, **kwargs)
