# -*- coding: utf-8 -*-
import datetime

import pytz
from flask import render_template, Blueprint

from module.site.page import Page
from module.site.site import Site

app = Blueprint("sitemap",
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは {{ url_for('sitemap.sitemap') }}
@app.route("/sitemap.xml")
def sitemap():
    """
    googleクローラー用のsitemap.xml
    """
    all_sites = Site.get_all()
    new_pages = Page.gets_new(10000)
    return render_template('sitemap/sitemap.html',
                           url_base='http://www.niku.tokyo/',
                           new_site_date=max([site.created_at for site in all_sites]),
                           all_sites=all_sites,
                           new_pages=new_pages,
                           one_days_ago=datetime.datetime.now() - datetime.timedelta(days=1),
                           three_days_ago=datetime.datetime.now() - datetime.timedelta(days=3),
                           )
