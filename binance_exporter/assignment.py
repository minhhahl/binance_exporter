import time
import json
from binance.spot import Spot
from prometheus_client import start_wsgi_server, Gauge
from data_processor import DataProcessor
from configs import *


class Assignment:
    def __init__(self):
        self._client = Spot()
        print(self._client.time())
        self._dp = DataProcessor()

        self.QUESTIONS = [
            '1. Print the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order.',
            '2. Print the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order.',
            '3. Using the symbols from Q1, what is the total notional value of the top 200 bids and asks currently on each order book?',
            '4. What is the price spread for each of the symbols from Q2?',
            '5. Every 10 seconds print the result of Q4 and the absolute delta from the previous value for each symbol.',
            '6. Make the output of Q5 accessible by querying http://localhost:8080/metrics using the Prometheus Metrics format.'
        ]

    def _get_ticker_24hr(self):
        """Call binance API to get the data

        API doc: https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#24hr-ticker-price-change-statistics

        Example response:
        [
            {
                "symbol": "BNBBTC",
                "priceChange": "-94.99999800",
                "priceChangePercent": "-95.960",
                "weightedAvgPrice": "0.29628482",
                "prevClosePrice": "0.10002000",
                "lastPrice": "4.00000200",
                "lastQty": "200.00000000",
                "bidPrice": "4.00000000",
                "askPrice": "4.00000200",
                "openPrice": "99.00000000",
                "highPrice": "100.00000000",
                "lowPrice": "0.10000000",
                "volume": "8913.30000000",
                "quoteVolume": "15.30000000",
                "openTime": 1499783499040,
                "closeTime": 1499869899040,
                "firstId": 28385,   // First tradeId
                "lastId": 28460,    // Last tradeId
                "count": 76         // Trade count
            }
        ]
        """

        res = self._client.ticker_24hr()

        return res

    def _get_order_book(self, symbol, api_limit=GET_BOOK_ORDER_API_LIMIT):
        """Call binance API to get the data

        API doc https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#market-data-endpoints

        Example response:
        {
            "lastUpdateId": 1027024,
            "bids": [
                [
                "4.00000000",     // PRICE
                "431.00000000"    // QTY
                ]
            ],
            "asks": [
                [
                "4.00000200",
                "12.00000000"
                ]
            ]
        }
        """

        res = self._client.depth(symbol=symbol, limit=api_limit)

        return res

    def _get_order_book_ticker(self, symbol):
        """Call binance API to get the data

        API doc: https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#symbol-order-book-ticker

        Example response:
        {
            "lastUpdateId": 1027024,
            "bids": [
                [
                "4.00000000",     // PRICE
                "431.00000000"    // QTY
                ]
            ],
            "asks": [
                [
                "4.00000200",
                "12.00000000"
                ]
            ]
        }
        """

        res = self._client.book_ticker(symbol=symbol)

        return res

    def _print_output(self, question_no, answer=None):
        print(self.QUESTIONS[question_no - 1])
        if answer:
            print(answer)
        print()

    def question1(self, output=False):
        ticker_24hr = self._get_ticker_24hr()
        res = self._dp.get_top_symbols(
            ticker_24hr,
            quote_asset='BTC',
            ranking_col='volume'
        )

        if output:
            self._print_output(1, res)

        return res

    def question2(self, output=False):
        ticker_24hr = self._get_ticker_24hr()
        res = self._dp.get_top_symbols(
            ticker_24hr,
            quote_asset='USDT',
            ranking_col='count'
        )

        if output:
            self._print_output(2, res)

        return res

    def _get_total_notinal_value(
        self,
        symbol,
        n=NOTIONAL_NUMBER_TOP_VALUE,
        target_cols=TARGET_COLS_TARGER_COLS
    ):
        res = self._get_order_book(symbol)
        res = list(map(
            lambda x: (x, self._dp.cal_total_notional_value(
                order_book=res,
                target_col=x,
                n=n)),
                target_cols
            ))

        return dict(res)

    def question3(self, target_cols=TARGET_COLS_TARGER_COLS, output=False):
        symbols = self.question1()
        res = [(s, self._get_total_notinal_value(
            symbol=s,
            target_cols=target_cols)) for s in symbols]

        res = dict(res)
        if output:
            self._print_output(3, json.dumps(res, indent=4))

        return res

    def _get_price_spread(self, symbol):
        res = self._get_order_book_ticker(symbol)

        return float(res['askPrice']) - float(res['bidPrice'])

    def question4(self, output=False):
        symbols = self.question2()
        res = [(s, self._get_price_spread(s)) for s in symbols]
        res = dict(res)

        if output:
            self._print_output(4, json.dumps(res, indent=4))

        return res

    def question5and6(self, answer4, output=True):
        self._print_output(5, "Check log in 10 seconds ...")
        self._print_output(6, "Please open http://localhost:8080/metrics on your browser")

        # Start up the server to expose the metrics.
        start_wsgi_server(EXPORTER_WEB_PORT)

        g_price_spread = Gauge('price_spread', 'Price spread of the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order', ['symbol'])
        g_price_spread_delta = Gauge('price_spread_detal', 'The absolute delta from the previous value for Price spread', ['symbol'])

        prev_res = answer4
        while True:
            time.sleep(PRICE_SPREAD_UPDATE_INTERVAL)
            res = self.question4()

            delta = {}
            for k, _ in res.items():
                # Have to check if the symbol is present in prev_res
                delta[k] = abs(res[k] - prev_res[k]) if k in prev_res else 0

                # Update metrics
                g_price_spread.labels(symbol=k).set(res[k])
                g_price_spread_delta.labels(symbol=k).set(delta[k])

            if output:
                print('Last price spread\n{}'.format(res))
                print('The absolute delta from the previous value\n{}'.format(delta))

            prev_res = res
