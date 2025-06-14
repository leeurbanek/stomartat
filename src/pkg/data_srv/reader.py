"""src/pkg/data_srv/reader.py\n
Collect open, high, low, close, volume \n
(ohlc) data from various online sources.\n
Returns a Pandas DataFrame.\n
class AlphaVantageReader\n
class TiingoReader\n
class YahooFinanceReader
"""
import datetime, time
import logging
import os

import pandas as pd
import requests

from random import randrange

from dotenv import load_dotenv

from pkg import DEBUG


load_dotenv()

logging.getLogger("urllib3").setLevel(logging.WARNING)
# logging.getLogger("yfinance").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class BaseReader:
    """"""
    def __init__(self, ctx:dict):
        self.data_provider = ctx['data_service']['data_provider']
        self.frequency = ctx['data_service']['data_frequency']
        self.index = ctx['interface']['index']
        self.lookback = int(ctx['data_service']['data_lookback'])
        self.start_date, self.end_date = self._start_end_date
        self.url = ctx['data_service'][f"url_{self.data_provider}"]


    @property
    def _start_end_date(self):
        """Set the start and end dates"""
        lookback = int(self.lookback)
        start = datetime.date.today() - datetime.timedelta(days=lookback)
        end = datetime.date.today()
        return start, end


    def get_ticker_df_tuple(self, ticker:str)->tuple[str, pd.DataFrame]:
        """Main entry point to class. Direct workflow of reader."""
        if DEBUG: logger.debug(f"{type(self)}, ticker={ticker}")

        raw_data = self._fetch_ohlc_price_data(ticker=ticker)
        parsed_data = self._parse_price_data(raw_data=raw_data)
        df = self._create_dataframe(parsed_data=parsed_data)

        return (ticker, df)


    def _create_dataframe(self, parsed_data: dict)->pd.DataFrame:
        """"""
        if DEBUG: logger.debug(f"_create_dataframe(self, parsed_data={parsed_data}) -> pd.DataFrame")
        df = pd.DataFrame.from_dict(
            data=parsed_data,
            orient='index',
            columns=['open', 'high', 'low', 'close', 'volume']
        )
        df.index.name='date'

        return df


    def _fetch_ohlc_price_data(self, ticker: str)->list[dict]:
        """Return ohlc price data in json format"""
        if DEBUG: logger.debug(f"_fetch_ohlc_price_data(ticker={ticker}) -> json")


    def _parse_price_data(self, raw_data:list[dict])->list[dict]:
        """Convert json ohlc data into price, volume, etc."""
        if DEBUG: logger.debug(f"_parse_price_data(self, raw_data={type(raw_data)}) -> list[dict]")


class AlphaVantageReader(BaseReader):
    """Fetch ohlc price data from tiingo.com"""

    def __init__(self, ctx:dict):
        super().__init__(ctx=ctx)
        self.api_token = os.getenv(f"API_TOKEN_{ctx['data_service']['data_provider'].upper()}")
        self.api_token_1 = os.getenv(f"API_TOKEN_{ctx['data_service']['data_provider'].upper()}_1")
        self.function = self._parse_frequency


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"api_token={self.api_token}, "
            f"api_token_1={self.api_token_1}, "
            f"data_provider={self.data_provider}, "
            f"frequency={self.frequency}, "
            f"function={self.function}, "
            f"index={self.index}, "
            f"lookback={self.lookback}, "
            f"start_date={self.start_date}, "
            f"end_date={self.end_date}, "
            f"url={self.url})"
            )


    @property
    def _parse_frequency(self):
        """Convert daily/weekly frequency to provider format"""
        frequency_dict ={'daily': 'TIME_SERIES_DAILY', 'weekly': 'TIME_SERIES_WEEKLY'}
        return frequency_dict[self.frequency]


    def _fetch_ohlc_price_data(self, ticker: str)->list[dict]:
        """Return ohlc price data in json format"""

        # output_size = 'compact'
        output_size = 'full'

        try:
            if self.index < 24:
                requestResponse = requests.get(
                    f"{self.url}/query?function={self.function}&symbol={ticker}&outputsize={output_size}&apikey={self.api_token}"
                )
            else:
                requestResponse = requests.get(
                    f"{self.url}/query?function={self.function}&symbol={ticker}&outputsize={output_size}&apikey={self.api_token_1}"
                )
        except requests.exceptions as e:
            logger.debug(f"*** ERROR *** {e}")

        if not((self.index + 1) % 5):
            for i in range(66, 0, -1):
                print(f"\tpausing for {i}... ", end='\r', flush=True)
                time.sleep(1)

        return requestResponse.json()


    def _parse_price_data(self, raw_data:list[dict])->list[dict]:
        """Convert json ohlc data into price, volume, etc."""
        ohlc_dict = dict()

        for key in raw_data['Time Series (Daily)']:
            value_dict = raw_data['Time Series (Daily)'][key]
            # if DEBUG: logger.debug(
            #     f"date: {datetime.date.fromisoformat(key)} {type(datetime.date.fromisoformat(key))}, start_date: {self.start_date} {type(self.start_date)}"
            # )
            if datetime.date.fromisoformat(key) < self.start_date:
                # print(f" *** break {key} ***")
                break
            date = round(time.mktime(datetime.datetime.strptime(key, '%Y-%m-%d').timetuple()))
            _open = round(float(value_dict.get('1. open'))*100)
            high = round(float(value_dict.get('2. high'))*100)
            low = round(float(value_dict.get('3. low'))*100)
            close = round(float(value_dict.get('4. close'))*100)
            volume = int(value_dict.get('5. volume'))
            ohlc_dict[date] = [_open, high, low, close, volume]

        ohlc_dict = dict(reversed(list(ohlc_dict.items())))

        return ohlc_dict


class TiingoReader(BaseReader):
    """Fetch ohlc price data from tiingo.com"""

    def __init__(self, ctx:dict):
        super().__init__(ctx=ctx)
        self.api_token = os.getenv(f"API_TOKEN_{ctx['data_service']['data_provider'].upper()}")
        self.frequency = ctx['data_service']['data_frequency']


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"api_token={self.api_token}, "
            f"frequency={self.frequency}, "
            f"index={self.index}, "
            f"lookback={self.lookback}, "
            f"start_date={self.start_date}, "
            f"url={self.url})"
            )


    def _fetch_ohlc_price_data(self, ticker: str)->list[dict]:
        """Return ohlc price data in json format"""

        try:
            requestResponse = requests.get(
                f"{self.url}/{self.frequency}/{ticker}/prices?startDate={self.start_date}"
                f"&token={self.api_token}", headers={'Content-Type': 'application/json'}
            )
            return requestResponse.json()
        except requests.exceptions as e:
            logger.debug(f"*** ERROR *** {e}")
        finally:
            time.sleep(randrange(1, 4))


    def _parse_price_data(self, raw_data:list[dict])->list[dict]:
        """Convert json ohlc data into price, volume, etc."""
        ohlc_dict = dict()

        for item in raw_data:
            date = round(time.mktime(datetime.datetime.strptime(item.get('date')[:10], '%Y-%m-%d').timetuple()))
            adjOpen = round(item.get('adjOpen')*100)
            adjHigh = round(item.get('adjHigh')*100)
            adjLow = round(item.get('adjLow')*100)
            adjClose = round(item.get('adjClose')*100)
            adjVolume = item.get('adjVolume')
            ohlc_dict[date] = [adjOpen, adjHigh, adjLow, adjClose, adjVolume]

        return ohlc_dict


class YahooFinanceReader(BaseReader):
    """Fetch ohlc price data using yfinance"""

    def __init__(self, ctx:dict):
        super().__init__(ctx=ctx)
        self.interval = self._parse_frequency


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"data_provider={self.data_provider}, "
            f"index={self.index}, "
            f"interval={self.interval}, "
            f"start_date={self.start_date}, "
            f"end_date={self.end_date})"
            )


    @property
    def _parse_frequency(self):
        """Convert daily/weekly frequency to provider format"""
        frequency_dict ={'daily': '1d', 'weekly': '1w'}
        return frequency_dict[self.frequency]


    def _fetch_ohlc_price_data(self, ticker: str)->dict[dict]:
        """Return ohlc price data in json format"""
        import yfinance as yf

        try:
            ticker = yf.Ticker(ticker)
            df = ticker.history(
                start=self.start_date, end=self.end_date, interval=self.interval
            )
            return df.to_json(orient='index')
        except Exception as e:
            logger.debug(f"*** ERROR *** {e}")


    def _parse_price_data(self, raw_data:dict[dict])->dict:
        """Convert json ohlc data into price, volume, etc."""
        import json

        ohlc_dict = dict()
        json_data = json.loads(raw_data)

        # print(f"\n**** raw_data: {raw_data} {type(raw_data)}")

        # for key in raw_data:
        for key in json_data:
            # print(f"\n**** key: {key} {type(key)}")

            value_dict = json_data[key]
            # print(f"\n**** json_data[key]: {json_data[key]} {type(json_data[key])}")

            Open = round(value_dict.get('Open')*100)
            High = round(value_dict.get('High')*100)
            Low = round(value_dict.get('Low')*100)
            Close = round(value_dict.get('Close')*100)
            Volume = value_dict.get('Volume')
            ohlc_dict[int(key)//1000] = [Open, High, Low, Close, Volume]

        return ohlc_dict

#     data = _select_data_provider(ctx=ctx, symbol=symbol)
#   File "/home/la/dev/stomartat/src/pkg/data_srv/client.py", line 74, in _select_data_provider
#     data = reader.get_ticker_df_tuple(ticker=symbol)
#   File "/home/la/dev/stomartat/src/pkg/data_srv/reader.py", line 55, in get_ticker_df_tuple
#     parsed_data = self._parse_price_data(raw_data=raw_data)
#   File "/home/la/dev/stomartat/src/pkg/data_srv/reader.py", line 265, in _parse_price_data
#     value_dict = raw_data[key]
# TypeError: string indices must be integers
