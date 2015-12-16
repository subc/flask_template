# -*- coding: utf-8 -*-
from flask_script import Command
from app import create_app
from module.scraping.inspection import InspectionWord
from module.site.page import Page, Keyword
from module.site.site import Site
from utils.db import get_db_engine

DatabaseTables = [
    Site,
    Page,
    Keyword,
    InspectionWord,
]


class MigrateDB(Command):
    """
    migrate database table
    """

    def run(self):
        print("start")
        self._migrate_db()
        print("finish")

    @property
    def app(self):
        return create_app()

    def _migrate_db(self):
        engine = get_db_engine()
        for db_cls in DatabaseTables:
            print('CREATE TABLE :{}'.format(db_cls.__name__))
            db_cls.metadata.create_all(engine)
