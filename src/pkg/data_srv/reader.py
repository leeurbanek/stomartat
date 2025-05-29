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

from dotenv import load_dotenv

from pkg import DEBUG


load_dotenv()

logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class BaseReader:
    """"""
    def __init__(self, ctx:dict):
        self.api_token = os.getenv(f"API_TOKEN_{ctx['data_service']['data_provider'].upper()}")
        self.data_provider = ctx['data_service']['data_provider']
        self.frequency = ctx['data_service']['data_frequency']
        self.function = self._parse_frequency
        self.lookback = int(ctx['data_service']['data_lookback'])
        self.start_date, self.end_date = self._start_end_date
        self.url = ctx['data_service'][f"url_{self.data_provider}"]


class AlphaVantageReader(BaseReader):
    """Fetch ohlc price data from tiingo.com"""

    def __init__(self, ctx:dict):
        super().__init__(ctx=ctx)
        # self.api_token = os.getenv(f"API_TOKEN_{ctx['data_service']['data_provider'].upper()}")
        # self.data_provider = ctx['data_service']['data_provider']
        # self.frequency = ctx['data_service']['data_frequency']
        # self.function = self._parse_frequency
        # self.lookback = int(ctx['data_service']['data_lookback'])
        # self.start_date, self.end_date = self._start_end_date
        # self.url = ctx['data_service'][f"url_{self.data_provider}"]


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"api_token={self.api_token}, "
            f"data_provider={self.data_provider}, "
            f"frequency={self.frequency}, "
            f"function={self.function}, "
            f"lookback={self.lookback}, "
            f"start_date={self.start_date}, "
            f"end_date={self.end_date}, "
            f"url={self.url})"
            )


    @property
    def _parse_frequency(self):
        """"""
        frequency_dict ={'daily': 'TIME_SERIES_DAILY', 'weekly': 'TIME_SERIES_WEEKLY'}
        return frequency_dict[self.frequency]


    @property
    def _start_end_date(self):
        """"""
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
        pass
        df = pd.DataFrame.from_dict(
            data=parsed_data,
            orient='index',
            columns=['open', 'high', 'low', 'close', 'volume']
        )
        df.index.name='date'
        if DEBUG: logger.debug(f"_create_dataframe(self, parsed_data) -> {type(df)}")
        return df


    def _fetch_ohlc_price_data(self, ticker: str)->list[dict]:
        """Return ohlc price data in json format"""
        if DEBUG: logger.debug(f"_fetch_ohlc_price_data(ticker={ticker})")

        output_size = 'compact'  # 'full'

        requestResponse = requests.get(
            f"{self.url}/query?function={self.function}&symbol={ticker}&outputsize={output_size}&apikey={self.api_token}"
        )
        return requestResponse.json()


    def _parse_price_data(self, raw_data:list[dict])->list[dict]:
        """"""
        ohlc_dict = dict()

        for key in raw_data['Time Series (Daily)']:
            value_dict = raw_data['Time Series (Daily)'][key]
            if DEBUG: logger.debug(
                f"date: {datetime.date.fromisoformat(key)} {type(datetime.date.fromisoformat(key))}, start_date: {self.start_date} {type(self.start_date)}"
            )
            if DEBUG: logger.debug(
                datetime.date.fromisoformat(key) < self.start_date
            )
            if datetime.date.fromisoformat(key) < self.start_date:
                break
            date = round(time.mktime(datetime.datetime.strptime(key, '%Y-%m-%d').timetuple()))
            _open = round(float(value_dict.get('1. open'))*100)
            high = round(float(value_dict.get('2. high'))*100)
            low = round(float(value_dict.get('3. low'))*100)
            close = round(float(value_dict.get('4. close'))*100)
            volume = int(value_dict.get('5. volume'))
            ohlc_dict[date] = [_open, high, low, close, volume]
        if DEBUG: logger.debug(f"_parse_price_data(self, dict_list)-> {type(ohlc_dict)}")

        ohlc_dict = dict(reversed(list(ohlc_dict.items())))
        return ohlc_dict


class TiingoReader(BaseReader):
    """Fetch ohlc price data from tiingo.com"""

    def __init__(self, ctx:dict):
        # super().__init__(ctx=ctx)
        self.api_token = os.getenv('API_TOKEN_TIINGO')
        self.data_provider = ctx['data_service']['data_provider']
        self.frequency = ctx['data_service']['data_frequency']
        self.lookback = int(ctx['data_service']['data_lookback'])
        self.start_date, self.end_date = self._start_end_date
        self.url = ctx['data_service'][f"url_{self.data_provider}"]


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"api_token={self.api_token}, "
            f"frequency={self.frequency}, "
            f"lookback={self.lookback}, "
            f"start_date={self.start_date}, "
            f"url={self.url})"
            )

    @property
    def _start_end_date(self):
        """"""
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
        df = pd.DataFrame.from_dict(
            data=parsed_data,
            orient='index',
            columns=['open', 'high', 'low', 'close', 'volume']
        )
        df.index.name='date'
        if DEBUG: logger.debug(f"_create_dataframe(self, parsed_data) -> {type(df)}")
        return df


    def _fetch_ohlc_price_data(self, ticker: str)->list[dict]:
        """Return ohlc price data in json format"""
        if DEBUG: logger.debug(f"_fetch_ohlc_price_data(ticker={ticker})")

        requestResponse = requests.get(
            f"{self.url}/{self.frequency}/{ticker}/prices?startDate={self.start_date}"
            f"&token={self.api_token}", headers={'Content-Type': 'application/json'}
        )
        return requestResponse.json()


    def _parse_price_data(self, raw_data:list[dict])->list[dict]:
        """"""
        ohlc_dict = dict()

        for item in raw_data:
            date = round(time.mktime(datetime.datetime.strptime(item.get('date')[:10], '%Y-%m-%d').timetuple()))
            adjOpen = round(item.get('adjOpen')*100)
            adjHigh = round(item.get('adjHigh')*100)
            adjLow = round(item.get('adjLow')*100)
            adjClose = round(item.get('adjClose')*100)
            adjVolume = item.get('adjVolume')
            ohlc_dict[date] = [adjOpen, adjHigh, adjLow, adjClose, adjVolume]
        if DEBUG: logger.debug(f"_parse_price_data(self, dict_list)-> {type(ohlc_dict)}")

        return ohlc_dict


class YahooFinanceReader(BaseReader):
    """Fetch ohlc price data using yfinance"""

    def __init__(self, ctx:dict):
        # super().__init__(ctx=ctx)
        self.data_provider = ctx['data_service']['data_provider']
        self.frequency = ctx['data_service']['data_frequency']
        self.interval = self._parse_frequency
        self.lookback = int(ctx['data_service']['data_lookback'])
        self.start_date, self.end_date = self._start_end_date

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"data_provider={self.data_provider}, "
            f"interval={self.interval}, "
            f"start_date={self.start_date}, "
            f"end_date={self.end_date})"
            )

    @property
    def _parse_frequency(self):
        """"""
        frequency_dict ={'daily': '1d', 'weekly': '1w'}
        return frequency_dict[self.frequency]


    @property
    def _start_end_date(self):
        """"""
        start = datetime.date.today() - datetime.timedelta(days=self.lookback)
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
        df = pd.DataFrame.from_dict(
            data=parsed_data,
            orient='index',
            columns=['open', 'high', 'low', 'close', 'volume']
        )
        df.index.name='date'
        if DEBUG: logger.debug(f"_create_dataframe(self, parsed_data) -> {type(df)}")
        return df


    def _fetch_ohlc_price_data(self, ticker: str)->dict[dict]:
        """Return ohlc price data in json format"""
        import yfinance as yf

        if DEBUG: logger.debug(f"_fetch_ohlc_price_data(self={self}, ticker={ticker})")

        ticker = yf.Ticker(ticker)
        df = ticker.history(start=self.start_date, end=self.end_date, interval=self.interval)

        return df.to_json(orient='index')


    def _parse_price_data(self, raw_data:dict[dict])->dict:
        """"""
        ohlc_dict = dict()

        for key in raw_data:
            value_dict = raw_data[key]
            Open = round(value_dict.get('Open')*100)
            High = round(value_dict.get('High')*100)
            Low = round(value_dict.get('Low')*100)
            Close = round(value_dict.get('Close')*100)
            Volume = value_dict.get('Volume')
            ohlc_dict[int(key)//1000] = [Open, High, Low, Close, Volume]
        if DEBUG: logger.debug(f"_parse_price_data(self, dict_list)-> {type(ohlc_dict)}")

        return ohlc_dict
