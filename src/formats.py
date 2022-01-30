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
    call = "call"
    put = "put"


class ExpirationType(Enum):
    intra = "intra"
    week = "week"
    month = "month"


class ExerciseType(Enum):
    american = "american"
    europe = "europe"





