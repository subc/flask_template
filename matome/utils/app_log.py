# -*- coding: utf-8 -*-
import datetime


def app_log(log_level, msg):
    prefix = '[{}] '.format(datetime.datetime.now())
    msg = prefix + msg

    from app import create_app
    _l = create_app().logger
    if log_level >= 50:
        _l.critical(msg)
    elif log_level >= 40:
        _l.error(msg)
    elif log_level >= 20:
        _l.debug(msg)
