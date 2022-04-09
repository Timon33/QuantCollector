import numpy as np
import pandas as pd
import logging
import os
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

    def save_dataframe(self, symbol: Symbol, interval: TimeInterval, data: pd.DataFrame, asset_class: AssetClass):
        item_name = f"{symbol.name}.{interval.name}"

        if isinstance(data.index, pd.MultiIndex):
            # kinda ugly way of getting the path from pystore
            path = self.store.collection(asset_class.value)._item_path(item_name, as_string=True)
            if os.path.isfile(path):
                data.to_csv(path, mode="ab", header=False, compression="zip")
            else:
                data.to_csv(path, mode="wb", header=True, compression="zip")
        else:
            if item_name not in self.store.collection(asset_class.value).items:
                self.store.collection(asset_class.value).write(item_name, data, metadata={"data_source": self.name})
            else:
                self.store.collection(asset_class.value).append(item_name, data)

    # saves all data provided by the api for the given symbol
    @ abstractmethod
    def download_all(self, symbol: Symbol, interval: TimeInterval):
        raise NotImplementedError

    @staticmethod
    def rename_dataframes(df: pd.DataFrame, renaming: dict, types: dict) -> pd.DataFrame:
        df = df.rename(columns=renaming, errors="ignore")
        df = df.reindex(columns=types.keys())
        # filter Nan values for types to be converted to int
        for c_name, c_type in types.items():
            if "int" in c_type:
                print("Null in type", c_name)
                df = df[df[c_name].notnull()]
        return df.astype(types)


class EquityAPI(API):

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
        price_data = self.rename_dataframes(
            price_data,
            self.api_conf["price_history_column_renaming"],
            config.get_dataframe_types("price_history")
        )
        self.save_dataframe(symbol, interval, price_data, AssetClass.options)

    def save_option_chains(self, symbol: Symbol, interval: TimeInterval) -> None:

        option_data = self.download_option_chains(symbol, interval)
        option_data = self.rename_dataframes(
            option_data,
            self.api_conf["option_chain_column_renaming"],
            config.get_dataframe_types("option_chain")
        )
        option_data = pd.concat({np.datetime64('today', "D"): option_data})
        self.save_dataframe(symbol, interval, option_data, AssetClass.options)

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
