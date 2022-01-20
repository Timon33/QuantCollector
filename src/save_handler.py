import json
import logging
import os
import datetime
import pytz

import config
import tradier_api
import shutil

logger = logging.getLogger(__name__)

# saves to file at the given location
# format

# {save_location}/{symbol}/{current date YYYY-MM-DD}/contracts.json - list of all available contracts for this day {
# save_location}/{symbol}/{current date YYYY-MM-DD}/{expiration date YYYY-MM-DD}.json - option chain for expiration
# date


def mkdir(location):
    if not os.path.isdir(location):
        os.mkdir(location)


# Timezone for NY (NYSE and NASDAQ)
def get_timezone(name="US/Eastern"):
    return pytz.timezone(name)


def get_date_string(date=None) -> str:
    date = datetime.datetime.now(get_timezone()) if date is None else date
    return str(date).split()[0]


# creates no existing folder and return path to save location for symbol
def get_save_location(symbol: str):
    save_location = config.get_config("save_location")
    mkdir(save_location)

    save_location = os.path.join(save_location, symbol)
    mkdir(save_location)

    logger.debug(f"Created folder {save_location}")

    return save_location


# contracts.json containing all option contract names for that day
def save_contract_list(api_key: str, symbol: str, save_location: str):
    contracts = tradier_api.lookup_options_symbols(api_key, symbol)

    with open(os.path.join(save_location, f"{get_date_string()}.json"), "w") as f:
        json.dump(contracts, f, indent=4)


# save the option chain for one expiration as one file
def save_option_chain(api_key: str, symbol: str, expiration: datetime, save_location: str):
    option_chain = tradier_api.get_option_chains(api_key, symbol, expiration)

    save_location = os.path.join(save_location, get_date_string())
    mkdir(save_location)
    with open(os.path.join(save_location, f"{get_date_string(expiration)}.json"), "w") as f:
        json.dump(option_chain, f, indent=4)


# save all the option chains for one symbol
def save_all_option_chains(api_key: str, symbol: str, location: str):
    if os.path.isfile(os.path.join(location, f"{get_date_string()}.zip")) and\
            str(config.get_config("overwrite_files")).lower() != "true":

        logger.warning(f"the file {location}.zip already exists! Skipping downloading data for symbol {symbol}")
        return

    expirations = tradier_api.get_options_expirations(api_key, symbol, strikes=False)
    try:
        expirations = expirations["expirations"]["date"]
    except Exception as e:
        logger.error(f"no options for symbol {symbol} found\n{e}")
        return

    expirations = list(map(lambda x: datetime.datetime.fromisoformat(x), expirations))

    # download the option chain for every expiration
    for exp in expirations:
        save_option_chain(api_key, symbol, exp, location)

    archive_name = os.path.join(location, get_date_string())
    shutil.make_archive(archive_name, "zip", archive_name)
    shutil.rmtree(archive_name)


def download_option_data(api_key: str):
    symbol_list = sorted(config.get_symbols())
    n_symbols = len(symbol_list)

    if n_symbols < 1:
        logger.critical("No Symbols in list! Aborting")
        exit(1)

    for i, symbol in enumerate(symbol_list):
        # progress info
        logger.info(f"{i + 1}/{n_symbols} ({(i + 1) / n_symbols * 100:.2f}%) downloading data for {symbol}...")

        save_location = get_save_location(symbol)

        # TODO finner error handling
        try:
            save_contract_list(api_key, symbol, save_location)
            save_all_option_chains(api_key, symbol, save_location)
        except IOError:
            logger.error(f"IO Error for symbol {symbol}")
        except json.JSONDecodeError:
            logger.error(f"Json Decode Error for symbol {symbol}")

