import json
import logging
import os
import datetime
import pytz
import config
from enum import Enum


class AssetClasses(Enum):
    equity = "equity"
    forex = "forex"
    crypto = "crypto"
    alternative = "alternative"
    bonds = "bonds"
    commodities = "commodities"


class TimeInterval(Enum):
    second = "second"
    minute = "minute"
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"
    quarter = "quarter"
    year = "year"


class TimeFrames(Enum):
    short_term = [TimeInterval.second, TimeInterval.minute, TimeInterval.hour]
    mid_term = [TimeInterval.day, TimeInterval.week, TimeInterval.month]
    long_term = [TimeInterval.quarter, TimeInterval.year]


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


logger = logging.getLogger(__name__)


def mkdir(location):
    if not os.path.isdir(location):
        os.mkdir(location)


# Timezone for NY (NYSE and NASDAQ)
def get_timezone(name="US/Eastern"):
    return pytz.timezone(name)


def get_date_string(date=None) -> str:
    date = datetime.datetime.now(get_timezone()) if date is None else date
    return date.strftime("%d-%m-%Y")


# creates no existing folder and return path to save location for symbol
def get_save_location(asset_class: AssetClasses, time_interval: TimeInterval, symbol: Symbol, timestamp: int):
    return os.path.join(config.get_config("save_location"), asset_class.value, symbol.asset_type, time_interval.value,
                        symbol.name, str(timestamp))


def rename_dict(dictionary: dict, rename: dict) -> dict:
    for k, v in rename.items():
        dictionary[v] = dictionary.pop(k)
    return dictionary
