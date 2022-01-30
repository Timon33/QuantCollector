import datetime
import json
import logging
import sys

import config
import data_util
from src.apis import tradier


# this script is called by cronjob or similar util
# uses api and config scripts

# setup for the logging module
# all loggers should be children of logger "main"
def logging_setup(stdout_logging_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    logfile_handler = logging.FileHandler(config.get_config()["logging_location"])

    stdout_handler.setLevel(stdout_logging_level)
    logfile_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    stdout_handler.setFormatter(formatter)
    logfile_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(logfile_handler)


def main():
    logging_setup(config.get_loglevel())
    logger = logging.getLogger("main")

    logger.warning("Starting downloads...")

    if market_status is not None:
        market_status["timestamp"] = datetime.datetime.fromtimestamp(market_status["timestamp"],
                                                                     save_handler.get_timezone()).strftime("%d.%m.%Y %X")
        logger.info(f"Current exchange status:\n{json.dumps(market_status, indent=4)}")
    else:
        logger.warning("Couldn't get current time from API")

    save_handler.download_option_data(api_secret)


if __name__ == "__main__":
    main()
