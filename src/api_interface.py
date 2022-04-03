import imp
from importlib.metadata import metadata
import os.path

import pandas as pd
import logging
from abc import ABC, abstractmethod

import config
import data_util
from data_util import Symbol, AssetClasses, TimeInterval

logger = logging.getLogger(__name__)


class API(ABC):

    name = "API_Base"

    def __init__(self) -> None:
        super().__init__()
        self.config = config.get_api(self.name)

    # saves all data provided by the api for the given symbol
    @abstractmethod
    def download_all(self, symbol: Symbol, interval: TimeInterval):
        pass


class EquityAPI(API):

    asset_class = AssetClasses.equity

    # overwriten by implementing subclass, column names/types api specific

    @abstractmethod
    def download_option_chains(self, symbol: Symbol, interval: TimeInterval) -> pd.DataFrame:
        pass

    @abstractmethod
    def download_price_history(self, symbol: Symbol, interval: TimeInterval) -> pd.DataFrame:
        pass

    @abstractmethod
    def download_fundamental_data(self, symbol: Symbol, interval: TimeInterval) -> pd.DataFrame:
        pass

    # convert data to common layout to be saved

    def get_price_history(self, symbol: Symbol, interval: TimeInterval) -> pd.DataFrame:
        dataframe = self.download_price_history(symbol, interval)
        return dataframe.rename(self.config["column_renaming"]).astype(config.get_dataframe_types("price_history"))

    def download_all(self, symbol: Symbol, interval: TimeInterval):
        logger.info(
            f"downloading equity data from {self.name} api for {symbol} with resolution {interval}")

        store = config.get_pystore()

        dataframe = self.get_price_history(symbol, interval)
        store.collection(self.asset_class.value).write(
            f"{symbol.name}.{interval.name}",
            dataframe,
            metadata={"data_source": self.name})


class ForexAPI(API):

    asset_class = AssetClasses.forex


class CryptoAPI(API):

    asset_class = AssetClasses.crypto


class AlternativeAPI(API):

    asset_class = AssetClasses.alternative


class BondsAPI(API):

    asset_class = AssetClasses.bonds


class CommoditiesAPI(API):

    asset_class = AssetClasses.commodities
