# -*- coding: utf-8 -*-
import time


def timeit(f):
    def timed(*args, **kw):
        # http://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te-ts))
        return result
    return timed