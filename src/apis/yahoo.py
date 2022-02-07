import pandas as pd
import yfinance
from src import config, data_util, api_interface
from src.data_util import TimeInterval


class YFinanceAPI(api_interface.EquityAPI):
    period_for_interval = {
        "1m": "7d",
        "2m": "60d",
        "1h": "730d",
        "1d": "max"
    }

    # -- API interface --

    def get_option_chains(self, symbol: str, interval: TimeInterval) -> pd.DataFrame:
        pass

    def get_price_history(self, symbol: str, interval: TimeInterval) -> pd.DataFrame:
        pass

    def get_fundamental_data(self, symbol: str, interval: TimeInterval) -> pd.DataFrame:
        pass
