import os.path

import pandas as pd
import logging
from abc import ABC, abstractmethod

from src import config
from src.data_util import Symbol, AssetClasses, TimeInterval, get_save_location, get_rounded_timestamp

logger = logging.getLogger(__name__)


class API(ABC):

    name = "API baseclass"

    # saves all data provided by the api for the given symbol
    @abstractmethod
    def download_all(self, symbol: Symbol, interval: TimeInterval):
        pass


class EquityAPI(API):

    asset_class = AssetClasses.equity

    # TODO consistent data formats across apis

    def get_option_chain_format(self):
        pass

    def get_price_history_format(self):
        pass

    def get_fundamental_data_format(self):
        pass

    @abstractmethod
    def get_option_chains(self, symbol: str, interval: TimeInterval) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_price_history(self, symbol: str, interval: TimeInterval) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_fundamental_data(self, symbol: str, interval: TimeInterval) -> pd.DataFrame:
        pass

    def download_all(self, symbol: Symbol, interval: TimeInterval):
        logger.info(f"downloading equity data from {self.name} api for {symbol} with resolution {interval}")
        option_save_path = get_save_location(self.asset_class, "options", interval, symbol)
        print(option_save_path)
        timestamp = get_rounded_timestamp(interval)
        with open(os.path.join(option_save_path, str(timestamp)), "w") as f:
            f.write(self.get_option_chains(symbol.name, interval).to_csv())


class ForexAPI(API):

    asset_class = AssetClasses.forex


class CryptoAPI(API):
    pass


class AlternativeAPI(API):
    pass


class BondsAPI(API):
    pass


class CommoditiesAPI(API):
    pass


