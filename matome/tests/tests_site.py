# -*- coding: utf-8 -*-
from module.scraping.search import SearchManager
from module.site.site import Site


def tests_site():
    # get_test
    assert(Site.get(1))


def tests_site_search():
    SearchManager.search(Site.get(1))
    raise