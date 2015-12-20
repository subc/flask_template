# -*- coding: utf-8 -*-
import threading
import functools

tls = threading.local()


def cached_tls(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            storage = tls.cache
        except AttributeError:
            tls.cache = {}
            storage = tls.cache
        key_func_name = args[0].__module__ + args[0].__name__ + func.__name__
        key = '{}:{}'.format(key_func_name, '-'.join([str(kwargs[_]) for _ in kwargs]))

        if key in storage:
            return storage.get(key)
        value = func(*args, **kwargs)
        storage[key] = value
        return value

    return wrapper
