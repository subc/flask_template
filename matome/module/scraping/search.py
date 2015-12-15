# -*- coding: utf-8 -*-


from module.scraping.subjects import Subject


class SearchManager(object):
    """
    スレッドを検索する
    """
    def search(self, site):
        subjects = Subject.get_from_url(site)
        method = getattr(self, site.name)
        r = method(subjects, site)

        # 参照を切る
        method = None
        del method
        return r

    def phantom(self, subjects, site):
        """
        ファンキル
        :param subjects: list[Subject]
        :param site: Site
        """
        keywords = [
            'ファンキル',
            'オブキル'
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

        print(subjects_dict)

        for key in subjects_dict:
            sub = subjects_dict[key]
            sub.execute_matome()

        return subject
