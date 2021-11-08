import numpy as np
import pandas as pd
from finrl.neo_finrl.data_processors.processor_alpaca import AlpacaProcessor
from finrl.neo_finrl.data_processors.processor_ccxt import CcxtProcessor
from finrl.neo_finrl.data_processors.processor_joinquant import JoinquantProcessor
from finrl.neo_finrl.data_processors.processor_wrds import WrdsProcessor
from finrl.neo_finrl.data_processors.processor_yahoofinance import YahooFinanceProcessor
from typing import List
from finrl.neo_finrl.data_processors.func import add_hyphen_for_date

class DataProcessor:
    def __init__(self, data_source, **kwargs):
        if data_source == "alpaca":
            try:
                API_KEY = kwargs.get("API_KEY")
                API_SECRET = kwargs.get("API_SECRET")
                APCA_API_BASE_URL = kwargs.get("APCA_API_BASE_URL")
                self.processor = AlpacaProcessor(API_KEY, API_SECRET, APCA_API_BASE_URL)
                print("AlpacaProcessor successfully connected")
            except BaseException:
                raise ValueError("Please input correct account info for alpaca!")

        elif data_source == "ccxt":
            self.processor = CcxtProcessor(data_source, **kwargs)

        elif data_source == "joinquant":
            self.processor = JoinquantProcessor(data_source, **kwargs)

        elif data_source == "wrds":
            self.processor = WrdsProcessor(data_source, **kwargs)

        elif data_source == "yahoofinance":
            self.processor = YahooFinanceProcessor(data_source, **kwargs)

        else:
            raise ValueError("Data source input is NOT supported yet.")

    def download_data(
        self, ticker_list: List[str], start_date: str, end_date: str, time_interval: str
    ) -> pd.DataFrame:
        df = self.processor.download_data(
            ticker_list=ticker_list,
            start_date=start_date,
            end_date=end_date,
            time_interval=time_interval,
        )
        return df

    def clean_data(self, df) -> pd.DataFrame:
        df = self.processor.clean_data(df)

        return df

    def add_technical_indicator(self, df, tech_indicator_list) -> pd.DataFrame:
        self.tech_indicator_list = tech_indicator_list
        df = self.processor.add_technical_indicator(df, tech_indicator_list)

        return df

    def add_turbulence(self, df) -> pd.DataFrame:
        df = self.processor.add_turbulence(df)

        return df

    def add_vix(self, df) -> pd.DataFrame:
        df = self.processor.add_vix(df)

        return df

    def df_to_array(self, df, if_vix) -> np.array:
        price_array, tech_array, turbulence_array = self.processor.df_to_array(
            df, self.tech_indicator_list, if_vix
        )
        # fill nan and inf values with 0 for technical indicators
        tech_nan_positions = np.isnan(tech_array)
        tech_array[tech_nan_positions] = 0
        tech_inf_positions = np.isinf(tech_array)
        tech_array[tech_inf_positions] = 0

        return price_array, tech_array, turbulence_array

if __name__ == "__main__":
    # import sys
    #
    # sys.path.append("..")
    # from finrl.neo_finrl.neofinrl_config import TRADE_START_DATE
    # from finrl.neo_finrl.neofinrl_config import TRADE_END_DATE
    # from finrl.neo_finrl.neofinrl_config import READ_DATA_FROM_LOCAL
    # from finrl.neo_finrl.neofinrl_config import PATH_OF_DATA

    # read_data_from_local = READ_DATA_FROM_LOCAL
    # path_of_data = '../' + PATH_OF_DATA

    path_of_data = "../" + "data"

    TRADE_START_DATE = "2021-09-01"
    TRADE_END_DATE = "2021-09-11"
    READ_DATA_FROM_LOCAL = 1


    username = "18117580099"  # should input your username
    password = "Bl2020quant"  # should input your password
    kwargs = {'username': username, 'password': password}
    e = DataProcessor(data_source="joinquant", **kwargs)

    # trade_days = e.calc_trade_days_by_joinquant(TRADE_START_DATE, TRADE_END_DATE)
    # stocknames = ["000612.XSHE", "601808.XSHG"]
    # data = e.download_data(
    #     stocknames, trade_days[0], trade_days[-1], READ_DATA_FROM_LOCAL, path_of_data
    # )

    data2 = e.download_data(ticker_list=["000612.XSHE", "601808.XSHG"], start_date=TRADE_START_DATE, end_date=TRADE_END_DATE, time_interval='1Day')
    # data3 = e.clean_data(data2)
    data4 = e.add_technical_indicator(data2, ['macd', 'close_30_sma'])
    data5 = e.add_vix(data4)
    data6 = e.add_turbulence(data5)


