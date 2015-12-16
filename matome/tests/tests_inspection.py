# -*- coding: utf-8 -*-
from module.scraping.inspection import InspectionWord


def tests_inspection():
    word = 'あんぱん'
    assert InspectionWord.inspection(word) == False

    word = '死'
    assert InspectionWord.inspection(word)

    word = 'チンポには絶対に負けない(プラグ)なキャラと'
    assert InspectionWord.inspection(word)

    for x in range(10000):
        assert InspectionWord.inspection(word)
