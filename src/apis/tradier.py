import requests
import json
import logging
import pandas as pd

from datetime import datetime
from enum import Enum, auto

from src import config, data_util, api_interface

logger = logging.getLogger(__name__)


class ApiType(Enum):
    live = "live"
    sandbox = "sandbox"


class TradierAPI(api_interface.EquityAPI):

    name = "tradier"

    def __init__(self):
        self.secret = config.get_secret(self.name)
        self.api_type = ApiType(config.get_api(self.name).get("api_type"))
        self.url = config.get_api(self.name).get("url")

    # properly convert the responses to json (dict) objects
    def get_to_json(self, endpoint, params) -> dict:
        try:
            response = requests.get(f"https://{self.api_type.value}.{self.url}{endpoint}",
                                    params=params,
                                    headers={"Authorization": f"Bearer {self.secret}", "Accept": "application/json"},
                                    timeout=5
                                    )
        except requests.exceptions.Timeout:
            logger.error(f"API request timed out! endpoint {endpoint} params {params}")
            return dict()

        # 2xx success status code
        # TODO handel other status codes correctly
        if response.status_code == 200:
            try:
                response_json = json.loads(response.text)
                return response_json
            except json.JSONDecodeError as e:
                logger.error(f"error parsing json response!\n{e}")
                return dict()

        # error
        else:
            logger.error("API did not return status code 200:")
            logger.error(response.status_code)
            logger.error(response.text)
            return dict()

    def get_options_expirations(self, symbol: str, include_all_roots: bool = True, strikes: bool = False):
        logger.debug(f"get options chain api request: sym {symbol}")

        params = {'symbol': symbol, 'includeAllRoots': str(include_all_roots).lower(), 'strikes': str(strikes).lower()}
        return self.get_to_json("/v1/markets/options/expirations", params)

    def lookup_options_symbols(self, underlying: str):
        logger.debug(f"get options chain api request: underlying {underlying}")

        params = {'underlying': underlying}
        return self.get_to_json("/v1/markets/options/lookup", params)

    def get_option_chains(self, symbol: str, interval: data_util.TimeInterval) -> pd.DataFrame:
        expiration = self.get_options_expirations(symbol)

        try:
            expiration = expiration["expirations"]["date"]
        except KeyError:
            logger.error(f"Cant get option expirations for {symbol}. Skipping!")
            return pd.DataFrame()

        # list containing options object
        data_frame = pd.DataFrame()
        for exp in expiration:
            params = {'symbol': symbol, 'expiration': exp, 'greeks': "true"}
            json_data = self.get_to_json("/v1/markets/options/chains", params)["options"]["option"]
            for contract in json_data:
                # flattens the "greeks" sub dict
                data_frame.append(pd.Series({**contract.pop("greeks"), **contract}), ignore_index=True)

        data_frame.set_index("symbol", inplace=True)
        return data_frame

    def get_price_history(self, symbol: str, interval: data_util.TimeInterval) -> pd.DataFrame:
        pass

    def get_fundamental_data(self, symbol: str, interval: data_util.TimeInterval) -> pd.DataFrame:
        pass

    def download_all(self):
        pass
