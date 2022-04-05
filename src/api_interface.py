import numpy as np
import pandas as pd
import logging
from abc import ABC, abstractmethod

import config
from data_util import Symbol, AssetClass, TimeInterval

logger = logging.getLogger(__name__)


class API(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.api_conf = config.get_api(self.name)
        self.store = config.get_pystore()

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def asset_class(self) -> AssetClass:
        raise NotImplementedError

    def save_dataframe(self, symbol: Symbol, interval: TimeInterval, data: pd.DataFrame):
        item_name = f"{symbol.name}.{interval.name}"
        if item_name not in self.store.collection(self.asset_class.value).items:
            self.store.collection(self.asset_class.value).write(
                item_name, data, metadata={"data_source": self.name})
        else:
            self.store.collection(
                self.asset_class.value).append(item_name, data)

    # saves all data provided by the api for the given symbol

    @ abstractmethod
    def download_all(self, symbol: Symbol, interval: TimeInterval):
        raise NotImplementedError


class EquityAPI(API):

    @ property
    def asset_class(self) -> AssetClass:
        return AssetClass.equity

    # overwriten by implementing subclass, column names/types api specific

    @ abstractmethod
    def download_price_history(self, symbol: Symbol, interval: TimeInterval) -> pd.DataFrame:
        pass

    @ abstractmethod
    def download_option_chains(self, symbol: Symbol, interval: TimeInterval) -> pd.DataFrame:
        pass

    @ abstractmethod
    def download_fundamental_data(self, symbol: Symbol, interval: TimeInterval) -> pd.DataFrame:
        pass

    # convert data to common layout to be saved

    def save_price_history(self, symbol: Symbol, interval: TimeInterval) -> None:
        data_format = config.get_dataframe_types("price_history")

        price_data = self.download_price_history(symbol, interval)
        # missing columns can be ignored, they will be filled with NaNs
        price_data = price_data.rename(
            columns=self.api_conf["price_history_column_renaming"], errors="ignore")
        # create missing columns
        price_data = price_data.reindex(columns=data_format.keys())
        # TODO dynamic filtering of nan values
        price_data = price_data[price_data.volume.notnull()]
        price_data = price_data.astype(data_format)
        self.save_dataframe(symbol, interval, price_data)

    def save_option_chains(self, symbol: Symbol, interval: TimeInterval) -> None:
        option_data = self.download_option_chains(symbol, interval)
        option_data = option_data.rename(self.api_conf["option_chain_column_renaming"]).astype(
            config.get_dataframe_types("option_chain"))
        self.save_dataframe(symbol, interval, option_data)

    def download_all(self, symbol: Symbol, interval: TimeInterval):
        logger.info(
            f"downloading equity data from {self.name} api for {symbol} with resolution {interval}")

        self.save_price_history(symbol, interval)


class ForexAPI(API):
    asset_class = AssetClass.forex


class CryptoAPI(API):
    asset_class = AssetClass.crypto


class AlternativeAPI(API):
    asset_class = AssetClass.alternative


class BondsAPI(API):
    asset_class = AssetClass.bonds


class CommoditiesAPI(API):
    asset_class = AssetClass.commodities
