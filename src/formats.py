from enum import Enum, auto
from dataclasses import dataclass
import datetime
from abc import ABC


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
    call = auto()
    put = auto()


class ExpirationType(Enum):
    intra = auto()
    week = auto()
    month = auto()


class ExerciseType(Enum):
    american = auto()
    europe = auto()


@dataclass
class OptionData:
    symbol: str
    option_type: OptionType
    strike: float
    in_the_money: bool
    volume: int
    bid: float
    ask: float
    open: float
    high: float
    low: float
    close: float
    last: float
    change: float
    expiration_date: datetime
    days_to_expiration: int
    change_percentage: float
    bid_size: int
    ask_size: int
    open_interest: int
    expiration_type: ExpirationType
    exercise_type: ExerciseType
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    phi: float
    bid_iv: float
    mid_iv: float
    ask_iv: float
    smv_vol: float


@dataclass
class PriceData:
    volume: int
    bid: float
    ask: float
    open: float
    high: float
    low: float
    close: float
    last: float
    dividends: float
    split: float


class FundamentalData(ABC):
    pass
