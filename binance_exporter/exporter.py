import argparse
import sys
import logging

from binance_exporter.assignment import Assignment
import binance_exporter.configs as cfg

class Exporter:
    """Binance exporter application
    """

    def __init__(self, args):
        self._args = args

    def run(self):
        logging.basicConfig(
            level=self._args.loglevel,
            format='[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d-%(funcName)s] %(message)s',
            datefmt='%H:%M:%S',
            stream=sys.stdout
        )

        logging.info('Start app with args {}'.format(self._args))

        assignment = Assignment()

        assignment.question1(output=True)
        assignment.question2(output=True)
        assignment.question3(output=True)
        answer4 = assignment.question4(output=True)
        assignment.question5and6(answer4, port=self._args.port, upate_inverval=self._args.update_interval, output=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--port', '-p',
        help='Exporter port number',
        type=int,
        default=cfg.EXPORTER_WEB_PORT
    )
    parser.add_argument(
        '--update-interval', '-i',
        help='Price spread update interval',
        type=int,
        default=cfg.PRICE_SPREAD_UPDATE_INTERVAL
    )

    parser.add_argument(
        '--loglevel', '-l'
        , help='Log level'
        , nargs='?'
        , choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
        , default='INFO'
    )
    args = parser.parse_args()

    exporter = Exporter(args)
    exporter.run()
