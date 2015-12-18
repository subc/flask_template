# -*- coding: utf-8 -*-
from module.scraping.inspection import InspectionWord, inspection_affiliate


def tests_inspection():
    word = 'あんぱん'
    assert InspectionWord.inspection(word) == False

    word = '死'
    assert InspectionWord.inspection(word)

    word = 'チンポには絶対に負けない(プラグ)なキャラと'
    assert InspectionWord.inspection(word)

    for x in range(10000):
        assert InspectionWord.inspection(word)


def tests_afi():
    word = 'あんぱん'
    assert inspection_affiliate(word) == False

    word = 'あふぃ'
    assert inspection_affiliate(word)

    word = 'アフィ'
    assert inspection_affiliate(word)

    word = 'アマルフィ'
    assert inspection_affiliate(word)

    word = 'アまるふぃ'
    assert inspection_affiliate(word)

    word = 'あかん、ゴムゴムのるふぃ'
    assert inspection_affiliate(word)

    word = 'あかん、ゴムゴムのルフィ'
    assert inspection_affiliate(word)

    word = 'あかん、ゴムゴムのルフーーィ'
    assert inspection_affiliate(word)

    word = 'クリック'
    assert inspection_affiliate(word)

    word = 'くりっく'
    assert inspection_affiliate(word)

    word = '広告'
    assert inspection_affiliate(word)
