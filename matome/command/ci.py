# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import requests
from flask_script import Command


class CI(Command):
    """
    Circle CIの試験用
    """
    def run(self):
        test_urls = [
            "http://127.0.0.1:5000/example/",
        ]

        for url in test_urls:
            get_test(url)
            print("OK!:{}".format(url))


def get_test(url):
    headers = {
        "content-type": "text/html; charset=UTF-8"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert "Error" not in response.text
