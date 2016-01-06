# -*- coding: utf-8 -*-
import datetime
from flask import render_template

from module.site.page import Page
from module.view_manager.view_util import generate_index_contents
from enum import Enum


def error_page(site, error):
    """
    :param site: Site
    :param error: ErrorPageCategory
    :return:
    """
    contents = Page(id=100000000,
                    site_id=site.id,
                    dat_id=0,
                    page=error.value,
                    page_top=error.value,
                    _keywords="",
                    created_at=datetime.datetime.now())
    svm = generate_index_contents(site)
    return render_template('dat/page.html',
                           contents=contents,
                           site=site,
                           svm=svm)


class ErrorPageCategory(Enum):
    DoesNotExist = "存在しないページです。"
    NotOpen = "非公開中のページです。"
