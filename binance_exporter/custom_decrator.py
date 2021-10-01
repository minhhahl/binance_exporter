import time
import traceback
from functools import wraps
import responses
import re

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

# Borrow from binance-connector-python repo at https://github.com/binance/binance-connector-python/blob/master/tests/util.py
def mock_http_response(
    method, uri, response_data, http_status=200, headers=None, body_data=""
):
    if headers is None:
        headers = {}

    def decorator(fn):
        @responses.activate
        def wrapper(*args, **kwargs):
            responses.add(
                method,
                re.compile(".*" + uri),
                json=response_data,
                body=body_data,
                status=http_status,
                headers=headers,
            )
            return fn(*args, **kwargs)

        return wrapper

    return decorator
