import logging

class DataProcessor:
    """Process Binance data
    """

    def __init__(self):
        pass

    def get_top_symbols(
        self,
        symbols,
        quote_asset,
        ranking_col,
        n=5,
        symbol_col_name='symbol'
    ):
        """Get top N sysbols by quote_asset by value of ranking_col

        Args:
            symbols (list): List of symbols' information that get from binance's API.
            quote_asset (str): Asset name. For example: BTC, USDT
            ranking_col (str): Colume name which is used for sorting the list of symbols. For example: volume, count
            n (int, optional): Limit top n results. Default 5.
            symbol_col_name (str, optional): Symbol colume's name in data. Default is 'symbol'.

        Returns:
            List of symbols' name
        """
        logging.debug("Call function")
        logging.debug(symbols, quote_asset, ranking_col, n, symbol_col_name)

        if symbols is None or len(symbols) == 0:
            logging.warning("List symbols is empty")
            return []

        # Filter symbols by quote_asset
        filted_list = list(filter(
            lambda x: quote_asset in x[symbol_col_name],
            symbols
        ))

        # Sort symbol by ranking_col in decreasing order
        sorted_list = sorted(
            filted_list,
            key=lambda x: float(x[ranking_col]),
            reverse=True
        )

        # Get top N items and return symbols's name
        symbols_list = list(map(lambda x: x[symbol_col_name], sorted_list[:n]))

        logging.debug("Return result {}".format(symbols_list))
        return symbols_list

    def cal_total_notional_value(self, order_book, target_col, n=200):
        """Calculate total notional value from order book of the top N notional on target_col

        Args:
            order_book (dict): A dictionary that contains lists of bids and asks. Example:
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
            target_col (str): Column's name which is used to calucate notional.
                              For example: bids, asks
            n (int, optional): limit top n results. Default 200.

        Returns:
            The total notional value
        """

        logging.debug('Call function')
        logging.debug(order_book, target_col, n)

        if order_book is None or len(order_book) == 0:
            logging.warning('Dictionary order_book is empty. Return 0')
            return 0

        if not target_col in order_book:
            logging.warning(
                "Dictionary order_book doesn't contain {} data".format(
                    target_col
                ))
            return 0

        # Loop to each item in target_col and calculate the notional
        # by multiple price and quatity
        notional_values = list(map(
            lambda x: float(x[0]) * float(x[1]),
            order_book[target_col]
        ))

        # Sorted notional by notional value in decreasing order
        sorted_list = sorted(
            notional_values,
            key=lambda x: x,
            reverse=True
        )

        # Get top N items and return sum of their values
        total_notional = sum(sorted_list[:n])

        logging.debug('Return result {}'.format(total_notional))

        return total_notional
