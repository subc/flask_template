# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from app import create_app
from command.migrate_db import MigrateDB

manager = Manager(create_app)

# manage.py option
manager.add_option('-c', '--config', dest='config', required=False)

# コマンド追加
manager.add_command('migrate', MigrateDB())
manager.add_command('runserver', Server(use_reloader=True))


if __name__ == "__main__":
    manager.run()
