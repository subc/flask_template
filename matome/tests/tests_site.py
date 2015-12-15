# -*- coding: utf-8 -*-
from module.site.site import Site


def tests_site():
    # get_test
    assert(Site.get(1))
