import argparse
from datetime import datetime


class ParserKit:

    @staticmethod
    def valid_datetime_start(s: str):
        if not s:
            return None

        try:
            return datetime.strptime(s.rstrip() + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            msg = "Not a valid date start: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def valid_datetime_end(s: str):
        if not s:
            return None
        try:
            return datetime.strptime(s.rstrip() + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            msg = "Not a valid date end: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)