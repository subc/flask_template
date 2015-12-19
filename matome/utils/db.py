# -*- coding: utf-8 -*-
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


tls = threading.local()


def get_db_session():
    """
    SQL Alchemy のDBセッションを生成して使い回す
    :rtype : scoped_session
    """
    if hasattr(tls, "db_session"):
        tls.counter += 1

        # 定期的にDBセッションをリセットする
        if tls.counter >= 10 * 10000:
            tls.db_session.close()
        else:
            return tls.db_session

    # DBセッションの生成
    engine = get_db_engine()
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    tls.db_session = db_session
    tls.counter = 0
    return db_session


def get_db_engine():
    # DBセッションの生成
    from app import create_app
    app = create_app()
    _db = app.config.get('DB')
    db_user = _db['user']
    db_host = _db['host']
    db_password = _db['password']
    db_name = _db['db_name']
    if db_password:
        db_path = 'mysql://{}:{}@{}/{}?charset=utf8'.format(db_user, db_password, db_host, db_name)
    else:
        db_path = 'mysql://{}@{}/{}?charset=utf8'.format(db_user, db_host, db_name)
    engine = create_engine(db_path, encoding='utf-8',
                           pool_size=1, max_overflow=1)
    return engine
