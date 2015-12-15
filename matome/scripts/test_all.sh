#!/bin/bash
# エラーなら停止
set -e
set -x

# module
py.test ./tests/tests_scraping.py
py.test ./tests/tests_site.py


# url

