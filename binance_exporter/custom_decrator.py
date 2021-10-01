import time
import traceback
from functools import wraps

def retry(ExceptionToCheck, tries=3, timeout=0, delay=1, backoff=1,
          show_log=False):
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            end_time = time.time() + timeout if timeout > 0 else 0
            mtries, mdelay = tries, delay
            while True:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    print("%s, Retrying in %s seconds..." % (str(e), mdelay))
                    if show_log:
                        traceback.print_exc()

                    if (end_time > 0 and time.time() > end_time) or\
                       (mtries > 0 and mtries <= 1):
                        raise(e)
                    elif mdelay > 0:
                        time.sleep(mdelay)

                    if mtries > 0:
                        mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


def waiting(ExceptionToCheck, timeout=10, delay=1, backoff=1, show_log=False):
    def deco_waiting(f):

        @wraps(f)
        def f_waiting(*args, **kwargs):
            end_time = time.time() + timeout if timeout > 0 else 0
            mdelay = delay
            while True:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    if show_log:
                        traceback.print_exc()

                    if end_time > 0 and time.time() > end_time:
                        raise(e)
                    elif mdelay > 0:
                        time.sleep(mdelay)

                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_waiting  # true decorator

    return deco_waiting
