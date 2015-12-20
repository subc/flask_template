# -*- coding: utf-8 -*-
debug = True

# database
DB = {
    'db_name': 'matome',
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'port': 3306
}

# redis
REDIS = {
    'default': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 6,
    }
}

# スクレイピングするスレッドの投稿数上限
SCRAPING_LIMIT = 950
