import json
import logging
import os

from datetime import datetime

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


def get_date_string() -> str:
    return str(datetime.today()).split()[0]


# creates no existing folder and return path to save location for symbol
def get_save_location(symbol: str):
    save_location = config.get_config()["save_location"]
    mkdir(save_location)

    save_location = os.path.join(save_location, symbol)
    mkdir(save_location)

    save_location = os.path.join(save_location, get_date_string())
    mkdir(save_location)

    return save_location


# contracts.json containing all option contract names for that day
def save_contract_list(api_key: str, symbol: str):
    save_location = get_save_location(symbol)
    if os.path.isfile(f"{save_location}.zip"):
        logger.warning(f"save file {save_location} already exists. Skipping download.")
        return

    contracts = tradier_api.lookup_options_symbols(api_key, symbol)

    with open(os.path.join(save_location, "contracts.json"), "w") as f:
        json.dump(contracts, f, indent=4)


# save the option chain for one expiration as one file
def save_option_chain(api_key: str, symbol: str, expiration: datetime):
    save_location = get_save_location(symbol)
    option_chain = tradier_api.get_option_chains(api_key, symbol, expiration)
    filename = f"{get_date_string()}.json"

    with open(os.path.join(save_location, filename), "w") as f:
        json.dump(option_chain, f, indent=4)


# save all the option chains for one symbol
def save_all_option_chains(api_key: str, symbol: str):
    location = get_save_location(symbol)
    if os.path.isfile(f"{location}.zip"):
        return

    expirations = tradier_api.get_options_expirations(api_key, symbol, strikes=False)
    try:
        expirations = expirations["expirations"]["date"]
    except Exception as e:
        logger.error(f"no options for symbol {symbol}\n{e}")
        return
    expirations = list(map(lambda x: datetime.fromisoformat(x), expirations))

    # download the option chain for every expiration
    for exp in expirations:
        save_option_chain(api_key, symbol, exp)

    shutil.make_archive(location, "zip", location)
    shutil.rmtree(location)


def download_option_data(api_key: str):
    symbol_list = config.get_config()["symbol_list_file"]
    n_symbols = len(symbol_list)

    for i, symbol in enumerate(symbol_list):
        # progress info
        logger.info(f"{i + 1}/{n_symbols} ({(i + 1) / n_symbols * 100:.2f}%) downloading data for {symbol}...")

        save_contract_list(api_key, symbol)
        save_all_option_chains(api_key, symbol)
