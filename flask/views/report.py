# -*- coding: utf-8 -*-
from flask import Module, render_template, Blueprint

app = Blueprint('report',
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは url_for('report.index')
@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    return 'report index'


# テンプレート内で呼び出すときは url_for('report.report_list')
@app.route('/report_list', methods=['GET'], strict_slashes=False)
def report_list():
    return 'report - list'
