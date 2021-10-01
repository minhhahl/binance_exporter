import unittest
from binance.spot import Spot as Client
from binance_exporter.assignment import Assignment
import responses
import re

MOCK_ITEM_01 = [
    {
        'input': [{
            'symbol': 'BTC{}'.format(i),
            'volume': i,
            'count': 10 - i
        } for i in range(0, 10)],
        'output': ['BTC9', 'BTC8', 'BTC7', 'BTC6', 'BTC5']
    },
    {
        'input': [{
            'symbol': '{}USDT'.format(i),
            'volume': i,
            'count': 10 - i
        } for i in range(0, 10)],
        'output': ['0USDT', '1USDT', '2USDT', '3USDT', '4USDT']
    }
]

MOCK_ITEM_02 = {
    'input': {
        "lastUpdateId": 1027024,
        "bids": [["4.0", "431.0"], ["1.0", "22.0"]],
        "asks": [["4.0", "12.0"], ["3.0", "2.0"]]
    },
    'output': {
        'BTC5': {'asks': 54.0, 'bids': 1746.0},
        'BTC6': {'asks': 54.0, 'bids': 1746.0},
        'BTC7': {'asks': 54.0, 'bids': 1746.0},
        'BTC8': {'asks': 54.0, 'bids': 1746.0},
        'BTC9': {'asks': 54.0, 'bids': 1746.0}
    }
}

MOCK_ITEM_03 = {
    'input': {
        "symbol": "",
        "bidPrice": "4.0",
        "bidQty": "431.00000000",
        "askPrice": "10.0",
        "askQty": "9.00000000"
    },
    'output': {'0USDT': 6.0, '1USDT': 6.0, '2USDT': 6.0, '3USDT': 6.0, '4USDT': 6.0}
}

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

class TestAssignment(unittest.TestCase):
    def setUp(self):
        self._a = Assignment()

    @mock_http_response(responses.GET, "/api/v3/ticker/24hr", MOCK_ITEM_01[0]['input'], 200)
    def test_question1(self):
        self.assertEqual(self._a.question1(output=True), MOCK_ITEM_01[0]['output'])

    @mock_http_response(responses.GET, "/api/v3/ticker/24hr", MOCK_ITEM_01[1]['input'], 200)
    def test_question2(self):
        self.assertEqual(self._a.question2(output=True), MOCK_ITEM_01[1]['output'])

    @mock_http_response(responses.GET, "/api/v3/ticker/24hr", MOCK_ITEM_01[0]['input'], 200)
    @mock_http_response(
        responses.GET, "/api/v3/depth\\?symbol=.*", MOCK_ITEM_02['input'], 200
    )
    def test_question3(self):
        self.assertEqual(self._a.question3(output=True), MOCK_ITEM_02['output'])


    @mock_http_response(responses.GET, "/api/v3/ticker/24hr", MOCK_ITEM_01[1]['input'], 200)
    @mock_http_response(
        responses.GET, "/api/v3/ticker/bookTicker\\?symbol=.*", MOCK_ITEM_03['input'], 200
    )
    def test_question4(self):
        self.assertEqual(self._a.question4(output=True), MOCK_ITEM_03['output'])
