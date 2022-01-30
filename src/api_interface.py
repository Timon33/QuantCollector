import pandas as pd

from abc import ABC, abstractmethod

from src import formats


class API(ABC):
    pass


class EquityAPI(API):

    @abstractmethod
    def download_option_chains(self, symbol: str, interval: formats.TimeInterval) -> pd.DataFrame:
        pass

    @abstractmethod
    def download_price_history(self, symbol: str, interval: formats.TimeInterval) -> pd.DataFrame:
        pass

    @abstractmethod
    def download_fundamental_data(self, symbol: str, interval: formats.TimeInterval) -> pd.DataFrame:
        pass


class ForexAPI(API):
    pass


class CryptoAPI(API):
    pass


class AlternativeAPI(API):
    pass


class BondsAPI(API):
    pass


class CommoditiesAPI(API):
    pass


