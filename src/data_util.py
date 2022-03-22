import json
import logging
import math
import os
import datetime
import pandas as pd
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

    def to_timedelta(self) -> datetime.timedelta:
        timedelta = _timedelta_map.get(self)
        return timedelta

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return id(self)


_timedelta_map = {
    TimeInterval.second: datetime.timedelta(seconds=1),
    TimeInterval.minute: datetime.timedelta(minutes=1),
    TimeInterval.hour: datetime.timedelta(hours=1),
    TimeInterval.day: datetime.timedelta(days=1),
    TimeInterval.week: datetime.timedelta(weeks=1)
}


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


# Timezone for NY (NYSE and NASDAQ)
def get_timezone(name="US/Eastern"):
    return pytz.timezone(name)


def get_date_string(date=None) -> str:
    date = datetime.datetime.now(get_timezone()) if date is None else date
    return date.strftime("%d-%m-%Y")


# round up to the next timestamp on the given timeinterval
def get_rounded_timestamp(interval: TimeInterval, date=None) -> int:
    date = datetime.datetime.now(get_timezone()) if date is None else date
    interval_seconds = int(interval.to_timedelta().total_seconds())
    return math.floor(date.timestamp()) // interval_seconds


# creates no existing folder and return path to save location for symbol
def get_save_location(asset_class: AssetClasses, asset_type: str, time_interval: TimeInterval, symbol: Symbol):
    path = os.path.join(config.get_config(
        "save_path"), asset_class.value, asset_type, time_interval.value, symbol.name)
    os.makedirs(os.path.abspath(path), exist_ok=True)
    return path
