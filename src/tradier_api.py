import requests
import json
import logging

from datetime import datetime

import config

logger = logging.getLogger(__name__)


# properly convert the responses to json (dict) objects
def get_to_json(endpoint, api_key, params):
    api_type = config.get_config()["api_type"]

    response = requests.get(f"https://{api_type}.tradier.com{endpoint}",
                            params=params,
                            headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
                            )

    # 2xx success status code
    # TODO handel other status codes correctly
    if response.status_code == 200:
        try:
            response_json = json.loads(response.text)
            return response_json
        except json.JSONDecodeError as e:
            logger.error(f"error parsing json response!\n{e}")
            return

    # error
    else:
        logger.error("API did not return status code 200:")
        logger.error(response.status_code)
        logger.error(response.text)
        return


# exactly matches the option related endpoints of the tradier api
# TODO reformat api calls and use config

def get_option_chains(api_key: str, symbol: str, expiration: datetime, greeks: bool = True):
    logger.debug(f"get options chain api request: sym {symbol}, expiration {expiration}, greeks {greeks}")

    params = {'symbol': symbol, 'expiration': str(expiration).split()[0], 'greeks': str(greeks).lower()}
    return get_to_json("/v1/markets/options/chains", api_key, params)


def get_option_strikes(api_key: str, symbol: str, expiration: datetime):
    logger.debug(f"get options chain api request: sym {symbol}, expiration {expiration}")

    params = {'symbol': symbol, 'expiration': str(expiration).split()[0]}
    return get_to_json("/v1/markets/options/strikes", api_key, params)


def get_options_expirations(api_key: str, symbol: str, include_all_roots: bool = True, strikes: bool = True):
    logger.debug(f"get options chain api request: sym {symbol}")

    params = {'symbol': symbol, 'includeAllRoots': str(include_all_roots).lower(), 'strikes': str(strikes).lower()}
    return get_to_json("/v1/markets/options/expirations", api_key, params)


def lookup_options_symbols(api_key: str, underlying: str):
    logger.debug(f"get options chain api request: underlying {underlying}")

    params = {'underlying': underlying}
    return get_to_json("/v1/markets/options/lookup", api_key, params)


# calendar api to know when to download option data
# defaults to current month
def get_calender(api_key: str, month: int = None, year: int = None):
    month = datetime.today().month if month is None else month
    year = datetime.today().year if year is None else year

    logger.debug(f"get options chain api request: month {month}, year {year}")

    params = {"month": month, "year": year}
    return get_to_json("/v1/markets/calendar", api_key, params)

# TODO add other api calls (fundamental data...)
