# -*- coding: utf-8 -*-
from command.insert_inspection import INSPECTION_WORD
from module.scraping.inspection import inspection_affiliate
from flask_script import Command, Option
from module.scraping.inspection import InspectionWord


class InspectionCheck(Command):
    """
    インスペクション辞書を登録する
    ベキ等性あり、連打可能
    """
    option_list = (
        Option('-w', '--word', required=False, help='inspeciton word'),
    )

    def run(self, word):
        if word is None:
            raise ValueError('word is None:  python manage.py check  --word="あいう"')

        # insert
        InspectionWord.register(INSPECTION_WORD)

        # ck
        if InspectionWord.inspection(word):
            print('True NGワードに該当')
            return
        if inspection_affiliate(word):
            print('True アフィチェックに該当')
            return
        print('False 該当せず')
