# -*- coding: utf-8 -*-
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


tls = threading.local()
POOL_SIZE = 5


def _get_db_session_id(count):
    return count % POOL_SIZE


def get_db_session():
    """
    SQL Alchemy のDBセッションを生成して使い回す
    :rtype : scoped_session
    """
    if hasattr(tls, "db_session"):
        tls.counter += 1
        _id = _get_db_session_id(tls.counter)

        session = tls.db_session.get(_id)
        if session:
            # 定期的にDBセッションをリセットする
            if tls.counter >= 10 * 10000:
                for _session in tls.db_session.values():
                    _session.close()
            else:
                return session
        else:
            session = _create_session()
            tls.db_session[_id] = session
            return session

    # 初回のみ
    tls.db_session = {}
    tls.counter = 0
    session = _create_session()
    tls.db_session[_get_db_session_id(0)] = session
    return session


def _create_session():
    # DBセッションの生成
    engine = get_db_engine()
    return scoped_session(sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine))


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
    engine = create_engine(db_path, encoding='utf-8')
    return engine
