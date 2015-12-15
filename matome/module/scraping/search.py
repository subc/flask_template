# -*- coding: utf-8 -*-


from module.scraping.subjects import Subject


class SearchManager(object):
    """
    スレッドを検索する
    """
    @classmethod
    def search(cls, site):
        method = getattr(cls, site.name)
        method(site)

        # 参照を切る
        method = None

    @classmethod
    def punk(cls, site):
        """
        ファンキル
        :param site: Site
        """
        print("Start ファンキル")
        subjects = Subject.get_from_url(site.url)

        print("Finish")
        pass
