# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import random
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
from module.site.site import Site


def tests_main():
    _tests_develop()
    _tests_production()
    

def _tests_develop():
    """
    開発環境の試験
    """
    host = "127.0.0.1:5000"
    url_base = "http://{}/{}/"
    site = random.choice(Site.get_all())
    test_url = url_base.format(host, site.title)
    parse_and_request(test_url)


def _tests_production():
    """
    本番環境の試験
    """
    host = "www.niku.tokyo"
    url_base = "http://{}/{}/"
    site = random.choice(Site.get_all())
    test_url = url_base.format(host, site.title)
    parse_and_request(test_url)


def parse_and_request(url):
    """
    urlをダウンロードして、bs4を解析して
    全リンクのステータスチェックする
    """
    # urlをパース
    o = urlparse(url)
    host = o.netloc

    # 指定されたURLをGETして解析
    response = requests.get(url, timeout=4)
    assert response.status_code == 200
    soup = BeautifulSoup(response.text, "lxml")
    test_urls = []
    for a in soup.find_all("a"):
        href = a.get("href")
        if href[0] == '#':
            pass
        elif href[0] == '/':
            # 相対リンク
            test_url = 'http://{}{}'.format(host, href)
            test_urls.append(test_url)
        elif host in href:
            # 絶対リンクかつ、同一ドメイン
            test_urls.append(href)
        else:
            # 外部サイトリンクはテストしない
            print('IGNORE:{}'.format(href))

    # 重複排除
    test_urls = list(set(test_urls))
    for test_url in test_urls:
        print(test_url)

    # リンクが生きているか非同期実行してチェック
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([check_url(url) for url in test_urls]))


async def check_url(url):
    """
    非同期でURLをチェックして、HTTP STATUSが200を応答することをチェック
    :param url: str
    """
    response = await aiohttp.request('GET', url)
    status_code = response.status
    assert status_code == 200, status_code
    response.close()
