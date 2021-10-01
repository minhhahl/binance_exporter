import argparse
import sys
import logging

from assignment import Assignment
import configs as cfg


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

    logging.basicConfig(
        level=args.loglevel,
        format='[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%H:%M:%S',
        stream=sys.stdout)

    logging.info('Start app with args {}'.format(args))

    assignment = Assignment()

    assignment.question1(output=True)
    assignment.question2(output=True)
    assignment.question3(output=True)
    answer4 = assignment.question4(output=True)
    assignment.question5and6(answer4, port=args.port, upate_inverval=args.update_interval, output=True)
