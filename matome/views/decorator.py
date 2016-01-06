# -*- coding: utf-8 -*-
import traceback
from functools import wraps
import datetime
from module.site.site import Site


def requires_site_title(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        site_title = kwargs.pop('site_title')
        try:
            site = Site.get_title(site_title)
        except IndexError:
            return 'error site_title does not exist'
        return f(site, **kwargs)
    return decorated_function


def err(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        エラーをログファイルに記録する
        """

        try:
            r = f(*args, **kwargs)
            return r
        except Exception as e:
            from app import create_app
            create_app().logger.critical(datetime.datetime.now())
            create_app().logger.critical(traceback.format_exc())
            raise e
    return decorated_function
