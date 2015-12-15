# -*- coding: utf-8 -*-
from module.scraping.storage import SearchStorage
from module.site.site import Site


def tests_scraping_storage():
    site = Site.get(1)
    s = SearchStorage(site)
    dat = 'test123'
    s.set_dat(dat)
    assert s.get_dat(dat) is not None
