# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from app import create_app
from command.insert_inspecton import InsertInspection
from command.inspecton_check import InspectionCheck
from command.migrate_db import MigrateDB
from command.scraping import Scraping
from command.search import Search

manager = Manager(create_app)

# manage.py option
manager.add_option('-c', '--config', dest='config', required=False)

# コマンド追加
manager.add_command('migrate', MigrateDB())
manager.add_command('scraping', Scraping())
manager.add_command('search', Search())
manager.add_command('sc', Scraping())
# inspectionコマンド
manager.add_command('inspection', InsertInspection())
manager.add_command('ins', InsertInspection())
manager.add_command('check', InspectionCheck())
manager.add_command('ck', InspectionCheck())
manager.add_command('runserver', Server(use_reloader=True))


if __name__ == "__main__":
    manager.run()
