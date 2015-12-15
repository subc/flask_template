# -*- coding: utf-8 -*-
from flask_script import Manager
from app import create_app
from command.migrate_db import MigrateDB

manager = Manager(create_app())

# コマンド追加
manager.add_command('migrate', MigrateDB())

if __name__ == "__main__":
    manager.run()
