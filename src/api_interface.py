import pandas as pd
from abc import ABC, abstractmethod

from src import data_util


class API(ABC):

    @abstractmethod
    def download_all(self):
        pass


class EquityAPI(API):

    asset_class = data_util.AssetClasses.equity

    @abstractmethod
    def get_option_chains(self, symbol: str, interval: data_util.TimeInterval) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_price_history(self, symbol: str, interval: data_util.TimeInterval) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_fundamental_data(self, symbol: str, interval: data_util.TimeInterval) -> pd.DataFrame:
        pass


class ForexAPI(API):

    asset_class = data_util.AssetClasses.forex


class CryptoAPI(API):
    pass


class AlternativeAPI(API):
    pass


class BondsAPI(API):
    pass


class CommoditiesAPI(API):
    pass


