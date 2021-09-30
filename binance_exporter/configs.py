import os

GET_BOOK_ORDER_API_LIMIT = int(os.getenv('GET_BOOK_ORDER_API_LIMIT', 5000))
NOTIONAL_NUMBER_TOP_VALUE = int(os.getenv('NOTIONAL_NUMBER_TOP_VALUE', 200))
EXPORTER_WEB_PORT = int(os.getenv('EXPORTER_WEB_PORT', 8080))
PRICE_SPREAD_UPDATE_INTERVAL = int(os.getenv('PRICE_SPREAD_UPDATE_INTERVAL', 10))
TARGET_COLS_TARGER_COLS = ['bids', 'asks']
