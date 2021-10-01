import unittest
from binance_exporter.data_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self._dp = DataProcessor()
        pass

    def test_get_top_symbols(self):
        test_cases = [
            {
                'input': [{
                    'symbol': 'BTC{}'.format(i),
                    'volume': i,
                    'count': 10 - i
                } for i in range(0, 10)],
                'output': ['BTC9', 'BTC8', 'BTC7', 'BTC6', 'BTC5'],
                'quote_asset': 'BTC',
                'ranking_col': 'volume'
            },
            {
                'input': [{
                    'symbol': '{}USDT'.format(i),
                    'volume': i,
                    'count': 10 - i
                } for i in range(0, 10)],
                'output': ['0USDT', '1USDT', '2USDT', '3USDT', '4USDT'],
                'quote_asset': 'USDT',
                'ranking_col': 'count'
            },
            {
                'input': [],
                'output': [],
                'quote_asset': 'BTC',
                'ranking_col': 'volume'
            },
            {
                'input': [{
                    'symbol': 'BTC{}'.format(i),
                    'volume': i,
                    'count': 10 - i
                } for i in range(0, 10)],
                'output': [],
                'quote_asset': 'NOT_FOUND_ASSET',
                'ranking_col': 'volume'
            },
        ]

        for t in test_cases:
            self.assertEqual(
                self._dp.get_top_symbols(
                    t['input'],
                    t['quote_asset'],
                    t['ranking_col']
                ),
                t['output']
            )

            t['input'] = [{
                'symbol': s['symbol'],
                'volume': str(s['volume']),
                'count': str(s['count'])
            } for s in t['input']]

            self.assertEqual(
                self._dp.get_top_symbols(
                    t['input'],
                    t['quote_asset'],
                    t['ranking_col']
                ),
                t['output']
            )

    def test_cal_total_notional_value(self):
        test_cases = [
            {
                'input': {
                    "lastUpdateId": 1027024,
                    "bids": [["4.0", "431.0"], ["1.0", "22.0"]],
                    "asks": [["4.0", "12.0"], ["3.0", "2.0"]]
                },
                'target_col': 'bids',
                'output': 4.0 * 431.0 + 1.0 * 22.0
            },
            {
                'input': {
                    "lastUpdateId": 1027024,
                    "bids": [["4.0", "431.0"], ["1.0", "22.0"]],
                    "asks": [["4.0", "12.0"], ["3.0", "2.0"]]
                },
                'target_col': 'asks',
                'output': 4.0 * 12.0 + 3.0 * 2.0
            },
            {
                'input': { "lastUpdateId": 1027024 },
                'target_col': 'asks',
                'output': 0
            },
            {
                'input': { "bids": [], "asks": [] },
                'target_col': 'asks',
                'output': 0
            }
        ]

        for t in test_cases:
            self.assertEqual(
                self._dp.cal_total_notional_value(t['input'], t['target_col']),
                t['output']
            )
