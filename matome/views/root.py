# -*- coding: utf-8 -*-
from flask import render_template, Blueprint

# 第一引数の名称が、テンプレのurl_for内で呼び出すときの名称と紐づく
from utils.db import get_db_session
from module.book import Book

app = Blueprint("index",
                __name__,
                url_prefix='/<user_url_slug>')


# テンプレート内で呼び出すときは url_for('index.index')
@app.route("/")
def index():
    book = get_db_session().query(Book).filter().all()
    # print(book)
    return render_template('root/index.html', book=book[0])
