import argparse
import logging

str_to_loglevel = {"DEBUG": logging.DEBUG,
                   "INFO": logging.INFO,
                   "WARNING": logging.WARNING,
                   "ERROR": logging.ERROR,
                   "CRITICAL": logging.CRITICAL}

parser = argparse.ArgumentParser()

parser.add_argument("--ll", "--logging-level", dest="logging_level", help="foo help", type=str,
                    choices=str_to_loglevel.keys())

parser.add_argument("options", help="foo help", type=str,
                    choices=str_to_loglevel.keys())

args = parser.parse_args()


def get_loglevel():
    return str_to_loglevel.get(args.loggin_level, default=logging.INFO)
