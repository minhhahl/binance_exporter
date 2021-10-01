import responses
import re

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
