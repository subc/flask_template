# -*- coding: utf-8 -*-


from module.scraping.subjects import Subject


class SearchManager(object):
    """
    スレッドを検索する
    """
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
        pass

        return subjects_dict
