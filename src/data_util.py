import logging
import datetime
import pandas as pd
from enum import Enum


class AssetClasses(Enum):
    equity = "equity"
    forex = "forex"
    crypto = "crypto"
    alternative = "alternative"
    bonds = "bonds"
    commodities = "commodities"


class TimeInterval(Enum):
    second = datetime.timedelta(seconds=1)
    minute = datetime.timedelta(minutes=1)
    hour = datetime.timedelta(hours=1)
    day = datetime.timedelta(days=1)

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return id(self)


class OptionType(Enum):
    call = "call"
    put = "put"


class ExpirationType(Enum):
    intra = "intra"
    week = "week"
    month = "month"


class ExerciseType(Enum):
    american = "american"
    europe = "europe"


class Symbol:

    def __init__(self, name: str, asset_type, exchange):
        self.name = name
        self.asset_type = asset_type
        self.exchange = exchange


TIMESERIES_DF_TYPES = {
    "volume": "int64",
    "bid": "float32",
    "ask": "float32",
    "open": "float32",
    "high": "float32",
    "low": "float32",
    "close": "float32",
    "last": "float32",
    "dividends": "float32",
    "split": "float32"
}


logger = logging.getLogger(__name__)
