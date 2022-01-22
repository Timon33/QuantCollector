import formats

from abc import ABC, abstractmethod


class API(ABC):
    pass


class EquityAPI(API):

    @abstractmethod
    def download_option_chains(self, symbol: str, interval: formats.TimeInterval) -> formats.OptionData:
        pass

    @abstractmethod
    def download_price_history(self, symbol: str, interval: formats.TimeInterval) -> formats.PriceData:
        pass

    @abstractmethod
    def download_fundamental_data(self, symbol: str, interval: formats.TimeInterval) -> formats.FundamentalData:
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


