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

    def __init__(self, ctx:dict):
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
        requestResponse = requests.get(
            f"{self.url}/{self.frequency}/{symbol}/prices?startDate={self.start_date}"
            f"&token={self.api_token}", headers={'Content-Type': 'application/json'}
        )
        dict_list = requestResponse.json()

        # EEM = [
        #     {'date': '2025-04-21T00:00:00.000Z', 'close': 41.91, 'high': 42.215, 'low': 41.6112, 'open': 42.17, 'volume': 16440713, 'adjClose': 41.91, 'adjHigh': 42.215, 'adjLow': 41.6112, 'adjOpen': 42.17, 'adjVolume': 16440713, 'divCash': 0.0, 'splitFactor': 1.0},
        #     {'date': '2025-04-22T00:00:00.000Z', 'close': 42.54, 'high': 42.825, 'low': 42.3401, 'open': 42.375, 'volume': 25716059, 'adjClose': 42.54, 'adjHigh': 42.825, 'adjLow': 42.3401, 'adjOpen': 42.375, 'adjVolume': 25716059, 'divCash': 0.0, 'splitFactor': 1.0},
        #     {'date': '2025-04-23T00:00:00.000Z', 'close': 43.03, 'high': 43.52, 'low': 42.98, 'open': 43.29, 'volume': 24787365, 'adjClose': 43.03, 'adjHigh': 43.52, 'adjLow': 42.98, 'adjOpen': 43.29, 'adjVolume': 24787365, 'divCash': 0.0, 'splitFactor': 1.0},
        #     {'date': '2025-04-24T00:00:00.000Z', 'close': 43.53, 'high': 43.58, 'low': 43.1, 'open': 43.15, 'volume': 28843537, 'adjClose': 43.53, 'adjHigh': 43.58, 'adjLow': 43.1, 'adjOpen': 43.15, 'adjVolume': 28843537, 'divCash': 0.0, 'splitFactor': 1.0},
        #     {'date': '2025-04-25T00:00:00.000Z', 'close': 43.45, 'high': 43.45, 'low': 43.135, 'open': 43.22, 'volume': 18363715, 'adjClose': 43.45, 'adjHigh': 43.45, 'adjLow': 43.135, 'adjOpen': 43.22, 'adjVolume': 18363715, 'divCash': 0.0, 'splitFactor': 1.0}
        # ]
        # IWM = [
        #     {'date': '2025-04-21T00:00:00.000Z', 'close': 182.74, 'high': 185.29, 'low': 180.765, 'open': 185.0, 'volume': 26018999, 'adjClose': 182.74, 'adjHigh': 185.29, 'adjLow': 180.765, 'adjOpen': 185.0, 'adjVolume': 26018999, 'divCash': 0.0, 'splitFactor': 1.0},
        #     {'date': '2025-04-22T00:00:00.000Z', 'close': 187.47, 'high': 188.1, 'low': 184.55, 'open': 185.15, 'volume': 34477053, 'adjClose': 187.47, 'adjHigh': 188.1, 'adjLow': 184.55, 'adjOpen': 185.15, 'adjVolume': 34477053, 'divCash': 0.0, 'splitFactor': 1.0},
        #     {'date': '2025-04-23T00:00:00.000Z', 'close': 190.25, 'high': 195.51, 'low': 189.84, 'open': 192.92, 'volume': 44866133, 'adjClose': 190.25, 'adjHigh': 195.51, 'adjLow': 189.84, 'adjOpen': 192.92, 'adjVolume': 44866133, 'divCash': 0.0, 'splitFactor': 1.0},
        #     {'date': '2025-04-24T00:00:00.000Z', 'close': 194.06, 'high': 194.37, 'low': 189.89, 'open': 190.76, 'volume': 29820132, 'adjClose': 194.06, 'adjHigh': 194.37, 'adjLow': 189.89, 'adjOpen': 190.76, 'adjVolume': 29820132, 'divCash': 0.0, 'splitFactor': 1.0},
        #     {'date': '2025-04-25T00:00:00.000Z', 'close': 194.12, 'high': 194.26, 'low': 191.55, 'open': 192.72, 'volume': 25028968, 'adjClose': 194.12, 'adjHigh': 194.26, 'adjLow': 191.55, 'adjOpen': 192.72, 'adjVolume': 25028968, 'divCash': 0.0, 'splitFactor': 1.0}
        # ]
        # dict_list = eval(symbol)

        if DEBUG: logger.debug(f"_fetch_ohlc_price_data(symbol={symbol})-> {type(dict_list)}")
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
        if DEBUG: logger.debug(f"_parce_price_data(self, dict_list)-> {type(data)}")
        return data
