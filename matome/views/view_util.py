# -*- coding: utf-8 -*-
from functools import wraps
from flask import g, flash, redirect, url_for, request
from module.site.site import Site


def requires_site_title(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        site_title = kwargs.pop('site_title')
        try:
            site = Site.get_title(site_title)
        except IndexError:
            # todo
            # return redirect(url_for('users.login', next=request.path))
            return 'error site_title does not exist'
        return f(site, **kwargs)
    return decorated_function
