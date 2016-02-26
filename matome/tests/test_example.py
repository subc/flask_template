# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import requests


def test_example():
    host = "127.0.0.1:5000"
    url = 'http://{}/example/'.format(host)
    print(url)
    response = requests.get(url)
    print(response.text)
    assert response.status_code == 200
    assert "Error" not in response.text
