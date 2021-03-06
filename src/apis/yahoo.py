import pandas as pd
import yfinance
import config
import data_util
import api_interface
from data_util import TimeInterval, Symbol


class YFinanceAPI(api_interface.EquityAPI):

    max_time_for_interval = {
        TimeInterval.minute: ("1m", "7d"),
        TimeInterval.hour: ("1h", "730d"),
        TimeInterval.day: ("1d", "max")
    }

    @property
    def name(self) -> str:
        return "yahoo"

    # -- API interface --

    def download_price_history(self, symbol: data_util.Symbol, interval: TimeInterval) -> pd.DataFrame:
        max_time = self.max_time_for_interval[interval]
        return yfinance.Ticker(symbol.name).history(
            interval=max_time[0], period=max_time[1], action=True, progress=False, prepost=True)

    def download_option_chains(self, symbol: Symbol, interval: TimeInterval) -> pd.DataFrame:
        pass

    def download_fundamental_data(self, symbol: Symbol, interval: TimeInterval) -> pd.DataFrame:
        pass
