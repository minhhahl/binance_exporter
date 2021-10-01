import unittest
import logging
import responses
from binance.spot import Spot as Client
from binance_exporter.assignment import Assignment
from binance_exporter.custom_decrator import mock_http_response

MOCK_ITEM_01 = [
    {
        'mock_data': [{
            'symbol': 'BTC{}'.format(i),
            'volume': i,
            'count': 10 - i
        } for i in range(0, 10)],
        'output': ['BTC9', 'BTC8', 'BTC7', 'BTC6', 'BTC5']
    },
    {
        'mock_data': [{
            'symbol': '{}USDT'.format(i),
            'volume': i,
            'count': 10 - i
        } for i in range(0, 10)],
        'output': ['0USDT', '1USDT', '2USDT', '3USDT', '4USDT']
    }
]

MOCK_ITEM_02 = {
    'mock_data': {
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
    'mock_data': {
        "symbol": "",
        "bidPrice": "4.0",
        "bidQty": "431.00000000",
        "askPrice": "10.0",
        "askQty": "9.00000000"
    },
    'output': {'0USDT': 6.0, '1USDT': 6.0, '2USDT': 6.0, '3USDT': 6.0, '4USDT': 6.0}
}

class TestAssignment(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

        self._a = Assignment(skip_api_ping=True)

    @mock_http_response(responses.GET, "/api/v3/ticker/24hr", MOCK_ITEM_01[0]['mock_data'], 200)
    def test_question1(self):
        self.assertEqual(self._a.question1(output=False), MOCK_ITEM_01[0]['output'])

    @mock_http_response(responses.GET, "/api/v3/ticker/24hr", MOCK_ITEM_01[1]['mock_data'], 200)
    def test_question2(self):
        self.assertEqual(self._a.question2(output=False), MOCK_ITEM_01[1]['output'])

    @mock_http_response(responses.GET, "/api/v3/ticker/24hr", MOCK_ITEM_01[0]['mock_data'], 200)
    @mock_http_response(
        responses.GET, "/api/v3/depth\\?symbol=.*", MOCK_ITEM_02['mock_data'], 200
    )
    def test_question3(self):
        self.assertEqual(self._a.question3(output=False), MOCK_ITEM_02['output'])

    @mock_http_response(responses.GET, "/api/v3/ticker/24hr", MOCK_ITEM_01[1]['mock_data'], 200)
    @mock_http_response(
        responses.GET, "/api/v3/ticker/bookTicker\\?symbol=.*", MOCK_ITEM_03['mock_data'], 200
    )
    def test_question4(self):
        self.assertEqual(self._a.question4(output=False), MOCK_ITEM_03['output'])
