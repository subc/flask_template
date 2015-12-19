# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from bs4 import BeautifulSoup
import requests


TEST_URLS = [
    "http://{}/fallout4/"
]


def tests_main():
    _tests_develop()
    _tests_production()
    

def _tests_develop():
    """
    開発環境の試験
    """
    host = "127.0.0.1:5000"
    for url_base in TEST_URLS:
        parse_and_request(url_base.format(host), host)


def _tests_production():
    """
    本番環境の試験
    """
    host = "www.niku.tokyo"
    for url_base in TEST_URLS:
        parse_and_request(url_base.format(host), host)


def parse_and_request(url, host):
    """
    urlをダウンロードして、bs4を解析して
    全リンクのステータスチェックする
    """
    response = requests.get(url, timeout=2)
    assert response.status_code == 200
    soup = BeautifulSoup(response.text, "lxml")
    for a in soup.find_all("a"):
        href = a.get("href")
        if href[0] == '/':
            test_url = 'http://{}{}'.format(host, href)
            print(test_url)
            req(test_url)


def req(url):
    response = requests.get(url, timeout=1)
    assert response.status_code == 200
