"""src/pkg/data_srv/reader.py\n
Collect open, high, low, close, volume \n
(ohlc) data from various online sources.\n
Returns a Pandas DataFrame.\n
class TiingoReader
"""
import datetime
import logging
import os

import pandas as pd
import requests

from dotenv import load_dotenv

from pkg import DEBUG


load_dotenv()
logger = logging.getLogger(__name__)


class TiingoReader:
    """Fetch ohlc price data from tiingo.com"""

    def __init__(self, ctx):
        self.api_token = os.getenv('API_TOKEN_TIINGO')
        self.ctx = ctx
        self.data_list = ctx['interface']['arguments']
        self.frequency = ctx['data_service']['data_frequency']
        self.lookback = ctx['data_service']['data_lookback']
        self.start_date = self._default_start_date
        self.url = self._url


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"api_token={self.api_token}, "
            f"data_list={self.data_list}, "
            f"frequency={self.frequency}, "
            f"lookback={self.lookback}, "
            f"start_date={self.start_date}, "
            f"url={self._url})"
            )

    @property
    def _default_start_date(self):
        """"""
        lookback = int(self.lookback)
        return datetime.date.today() - datetime.timedelta(days=lookback)


    @property
    def _url(self):
        """API url"""
        data_provider = self.ctx['data_service']['data_provider']
        return self.ctx['data_service'][f"url_{data_provider}"]


    def data_reader(self, symbol:str)->tuple[str, pd.DataFrame]:
        """Main entry point to class. Direct workflow of reader."""
        if DEBUG: logger.debug(f"{type(self)}, symbol={symbol}")

        dict_list = self._fetch_ohlc_price_data(symbol=symbol)
        parsed_data = self._parce_price_data(dict_list=dict_list)
        df = self._create_dataframe(parsed_data=parsed_data)

        return (symbol, df)


    def _create_dataframe(self, parsed_data: dict)->pd.DataFrame:
        """"""
        df = pd.DataFrame.from_dict(
            data=parsed_data,
            orient='index',
            columns=['open', 'high', 'low', 'close', 'volume']
        )
        df.index.name='date'
        if DEBUG: logger.debug(f"_create_dataframe(self, parsed_data) -> {type(df)}")
        return df


    def _fetch_ohlc_price_data(self, symbol: str)->list:
        """Return ohlc price data in json format"""
        # requestResponse = requests.get(
        #     f"{self.url}/{self.frequency}/{symbol}/prices?startDate={self.start_date}"
        #     f"&token={self.api_token}", headers={'Content-Type': 'application/json'}
        # )
        # dict_list = requestResponse.json()

        EEM = [{'date': '2025-04-21T00:00:00.000Z', 'close': 41.91, 'high': 42.215, 'low': 41.6112, 'open': 42.17, 'volume': 16440713, 'adjClose': 41.91, 'adjHigh': 42.215, 'adjLow': 41.6112, 'adjOpen': 42.17, 'adjVolume': 16440713, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-22T00:00:00.000Z', 'close': 42.54, 'high': 42.825, 'low': 42.3401, 'open': 42.375, 'volume': 25716059, 'adjClose': 42.54, 'adjHigh': 42.825, 'adjLow': 42.3401, 'adjOpen': 42.375, 'adjVolume': 25716059, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-23T00:00:00.000Z', 'close': 43.03, 'high': 43.52, 'low': 42.98, 'open': 43.29, 'volume': 24787365, 'adjClose': 43.03, 'adjHigh': 43.52, 'adjLow': 42.98, 'adjOpen': 43.29, 'adjVolume': 24787365, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-24T00:00:00.000Z', 'close': 43.53, 'high': 43.58, 'low': 43.1, 'open': 43.15, 'volume': 28843537, 'adjClose': 43.53, 'adjHigh': 43.58, 'adjLow': 43.1, 'adjOpen': 43.15, 'adjVolume': 28843537, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-25T00:00:00.000Z', 'close': 43.45, 'high': 43.45, 'low': 43.135, 'open': 43.22, 'volume': 18363715, 'adjClose': 43.45, 'adjHigh': 43.45, 'adjLow': 43.135, 'adjOpen': 43.22, 'adjVolume': 18363715, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-28T00:00:00.000Z', 'close': 43.53, 'high': 43.585, 'low': 43.32, 'open': 43.51, 'volume': 11002235, 'adjClose': 43.53, 'adjHigh': 43.585, 'adjLow': 43.32, 'adjOpen': 43.51, 'adjVolume': 11002235, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-29T00:00:00.000Z', 'close': 43.65, 'high': 43.76, 'low': 43.56, 'open': 43.59, 'volume': 12809121, 'adjClose': 43.65, 'adjHigh': 43.76, 'adjLow': 43.56, 'adjOpen': 43.59, 'adjVolume': 12809121, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-30T00:00:00.000Z', 'close': 43.76, 'high': 43.83, 'low': 43.405, 'open': 43.59, 'volume': 20928833, 'adjClose': 43.76, 'adjHigh': 43.83, 'adjLow': 43.405, 'adjOpen': 43.59, 'adjVolume': 20928833, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-05-01T00:00:00.000Z', 'close': 43.75, 'high': 43.96, 'low': 43.705, 'open': 43.93, 'volume': 14740506, 'adjClose': 43.75, 'adjHigh': 43.96, 'adjLow': 43.705, 'adjOpen': 43.93, 'adjVolume': 14740506, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-05-02T00:00:00.000Z', 'close': 45.0, 'high': 45.17, 'low': 44.835, 'open': 45.15, 'volume': 33945930, 'adjClose': 45.0, 'adjHigh': 45.17, 'adjLow': 44.835, 'adjOpen': 45.15, 'adjVolume': 33945930, 'divCash': 0.0, 'splitFactor': 1.0}]
        IWM = [{'date': '2025-04-21T00:00:00.000Z', 'close': 182.74, 'high': 185.29, 'low': 180.765, 'open': 185.0, 'volume': 26018999, 'adjClose': 182.74, 'adjHigh': 185.29, 'adjLow': 180.765, 'adjOpen': 185.0, 'adjVolume': 26018999, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-22T00:00:00.000Z', 'close': 187.47, 'high': 188.1, 'low': 184.55, 'open': 185.15, 'volume': 34477053, 'adjClose': 187.47, 'adjHigh': 188.1, 'adjLow': 184.55, 'adjOpen': 185.15, 'adjVolume': 34477053, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-23T00:00:00.000Z', 'close': 190.25, 'high': 195.51, 'low': 189.84, 'open': 192.92, 'volume': 44866133, 'adjClose': 190.25, 'adjHigh': 195.51, 'adjLow': 189.84, 'adjOpen': 192.92, 'adjVolume': 44866133, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-24T00:00:00.000Z', 'close': 194.06, 'high': 194.37, 'low': 189.89, 'open': 190.76, 'volume': 29820132, 'adjClose': 194.06, 'adjHigh': 194.37, 'adjLow': 189.89, 'adjOpen': 190.76, 'adjVolume': 29820132, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-25T00:00:00.000Z', 'close': 194.12, 'high': 194.26, 'low': 191.55, 'open': 192.72, 'volume': 25028968, 'adjClose': 194.12, 'adjHigh': 194.26, 'adjLow': 191.55, 'adjOpen': 192.72, 'adjVolume': 25028968, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-28T00:00:00.000Z', 'close': 194.94, 'high': 196.15, 'low': 192.53, 'open': 194.5, 'volume': 22482254, 'adjClose': 194.94, 'adjHigh': 196.15, 'adjLow': 192.53, 'adjOpen': 194.5, 'adjVolume': 22482254, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-29T00:00:00.000Z', 'close': 196.09, 'high': 196.86, 'low': 193.01, 'open': 194.47, 'volume': 20118155, 'adjClose': 196.09, 'adjHigh': 196.86, 'adjLow': 193.01, 'adjOpen': 194.47, 'adjVolume': 20118155, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-04-30T00:00:00.000Z', 'close': 194.86, 'high': 195.48, 'low': 190.721, 'open': 193.14, 'volume': 29046138, 'adjClose': 194.86, 'adjHigh': 195.48, 'adjLow': 190.721, 'adjOpen': 193.14, 'adjVolume': 29046138, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-05-01T00:00:00.000Z', 'close': 196.07, 'high': 197.67, 'low': 193.74, 'open': 195.71, 'volume': 33169717, 'adjClose': 196.07, 'adjHigh': 197.67, 'adjLow': 193.74, 'adjOpen': 195.71, 'adjVolume': 33169717, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2025-05-02T00:00:00.000Z', 'close': 200.48, 'high': 201.21, 'low': 198.18, 'open': 198.33, 'volume': 30201787, 'adjClose': 200.48, 'adjHigh': 201.21, 'adjLow': 198.18, 'adjOpen': 198.33, 'adjVolume': 30201787, 'divCash': 0.0, 'splitFactor': 1.0}]
        dict_list = eval(symbol)

        if DEBUG: logger.debug(f"_fetch_ohlc_price_data(symbol={symbol}) -> \n{dict_list}")
        return dict_list


    def _parce_price_data(self, dict_list:list[dict])->dict:
        """"""
        data = dict()
        ohlc = list()
        for item in dict_list:
            date = datetime.date.fromisoformat(item.get('date')[:10]).toordinal()
            adjOpen = round(item.get('adjOpen')*100)
            adjHigh = round(item.get('adjHigh')*100)
            adjLow = round(item.get('adjLow')*100)
            adjClose = round(item.get('adjClose')*100)
            adjVolume = item.get('adjVolume')
            data[date] = [adjOpen, adjHigh, adjLow, adjClose, adjVolume]
            ohlc.append(data)
        if DEBUG: logger.debug(f"_parce_price_data(self, dict_list) -> \n{data}")
        return data
