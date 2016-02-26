# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from flask_script import Command


class CI(Command):
    """
    Circle CI用
    """
    def run(self):
        print('HelloWorld!')
