"""src/pkg/data_srv/agent.py\n
Collect open, high, low, close, volume \n
(ohlc) data from various online sources.\n
Process data into lines; volume, average price,\n
close location value, etc. Returns a named tuple.\n
class AlphaVantageDataProcessor\n
class TiingoDataProcessor\n
class YahooFinanceDataProcessor
"""

import datetime, time
import logging
import os

import pandas as pd

from dotenv import load_dotenv

from pkg import DEBUG


load_dotenv()

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("yfinance").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class BaseProcessor:
    """"""

    def __init__(self, ctx: dict):
        self.data_line = ctx["data_service"]["data_line"]
        self.data_provider = ctx["data_service"]["data_provider"]
        self.frequency = ctx["data_service"]["data_frequency"]
        self.index = ctx["interface"]["index"]
        self.lookback = int(ctx["data_service"]["data_lookback"])
        self.start_date, self.end_date = self._start_end_date
        self.url = ctx["data_service"][f"url_{self.data_provider}"]

    @property
    def _start_end_date(self):
        """Set the start and end dates"""
        lookback = int(self.lookback)
        start = datetime.date.today() - datetime.timedelta(days=lookback)
        end = datetime.date.today()
        return start, end

    def fetch_and_parce_price_data(self, ticker: str):
        """"""
        if DEBUG:
            logger.debug(f"fetch_and_parce_price_data(self={type(self)}, ticker={ticker})")

        # data_gen = eval(f"_{self.data_provider}_data_generator(ticker=ticker)")
        # tuple_list = eval(f"_process_{self.data_provider}_data(data_gen=data_gen)")
        # return tuple_list


class AlphaVantageDataProcessor(BaseProcessor):
    """Fetch ohlc price data from alphavantage.com"""

    import requests
    from datetime import datetime as dt

    def __init__(self, ctx: dict):
        super().__init__(ctx=ctx)
        self.api_key = os.getenv(f"API_TOKEN_{self.data_provider.upper()}")
        self.api_key_1 = os.getenv(f"API_TOKEN_{self.data_provider.upper()}_1")
        self.function = self._parse_frequency

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"api_key={self.api_key}, "
            f"api_key_1={self.api_key_1}, "
            f"data_provider={self.data_provider}, "
            f"function={self.function}, "
            f"index={self.index}, "
            f"url={self.url})"
        )

    @property
    def _parse_frequency(self):
        """Convert daily/weekly frequency to provider format"""
        frequency_dict = {"daily": "TIME_SERIES_DAILY", "weekly": "TIME_SERIES_WEEKLY"}
        return frequency_dict[self.frequency]

    def _alphavantage_data_generator(self, ticker: str) -> object:
        """"""
        if DEBUG:
            logger.debug(f"_fetch_alphavantage_data(ticker={ticker})")

        API_URL = self.url

        params = {
            "function": self.function,
            "symbol": ticker,
            "outputsize": "compact",
            # output_size = "full"
            "datatype": "json",
            "apikey": self.api_key,
        }

        try:
            # params['apikey'] = self.api_key if self.index < 24 else self.api_key_1  # site throttles at 25 downloads
            r = self.requests.get(API_URL, params=params)
        except Exception as e:
            logger.debug(f"*** ERROR *** {e}")
        else:
            if not DEBUG:
                print(f" downloading '{ticker}'")
            yield r.json()
        # finally:  # pause after five downloads
        #     if not((index + 1) % 5):
        #         for i in range(63, 0, -1):
        #             print(f" pausing for {i} ", end='\r', flush=True)
        #             time.sleep(1)

    def _process_alphavantage_data(self, data_gen: object) -> list[tuple]:
        """"""
        if DEBUG:
            logger.debug(f"_process_alphavantage_data(data_gen={type(data_gen)})")

        alphavantage_dict = next(data_gen)
        ticker = alphavantage_dict["Meta Data"]["2. Symbol"]
        time_series_dict = alphavantage_dict["Time Series (Daily)"]

        if DEBUG:
            logger.debug(f"ticker: {ticker}, type(time_series_dict): {type(time_series_dict)}\n{time_series_dict}")

        # create empty dataframe with index as a timestamp
        df = pd.DataFrame(
            index=[round(time.mktime(self.dt.strptime(d[:10], "%Y-%m-%d").timetuple())) for d in time_series_dict]
        )
        df.index.name = "date"

        # add the data lines to dataframe
        def add_clop_series(loc: int) -> None:
            """difference between the close and open price"""
            if DEBUG:
                logger.debug(f"add_clop_series(loc={loc})")
            series_list = list()
            for i in time_series_dict:
                open_ = float(time_series_dict[i]["1. open"])
                close = float(time_series_dict[i]["4. close"])
                series_list.append(round((close - open_) * 100))
            df.insert(loc=loc, column="clop", value=series_list, allow_duplicates=True)

        def add_clv_series(loc: int) -> None:
            """close location value, relative to the high-low range"""
            if DEBUG:
                logger.debug(f"add_clv_series(loc={loc})")
            series_list = list()
            for i in time_series_dict:
                high = float(time_series_dict[i]["2. high"])
                low = float(time_series_dict[i]["3. low"])
                close = float(time_series_dict[i]["4. close"])
                try:
                    series_list.append(round(((2 * close - low - high) / (high - low)) * 100))
                except ZeroDivisionError as e:
                    logger.debug(f"*** ERROR *** {e}")
            df.insert(loc=loc, column="clv", value=series_list, allow_duplicates=True)

        def add_cwap_series(loc: int) -> None:
            """close weighted average price excluding open price"""
            if DEBUG:
                logger.debug(f"add_cwap_series(loc={loc})")
            series_list = list()
            for i in time_series_dict:
                high = float(time_series_dict[i]["2. high"])
                low = float(time_series_dict[i]["3. low"])
                close = float(time_series_dict[i]["4. close"])
                series_list.append(round(((high + low + close * 2) / 4) * 100))
            df.insert(loc=loc, column="cwap", value=series_list, allow_duplicates=True)

        def add_hilo_series(loc: int) -> None:
            """difference between the high and low price"""
            if DEBUG:
                logger.debug(f"add_hilo_series(loc={loc})")
            series_list = list()
            for i in time_series_dict:
                high = float(time_series_dict[i]["2. high"])
                low = float(time_series_dict[i]["3. low"])
                series_list.append(round((high - low) * 100))
            df.insert(loc=loc, column="hilo", value=series_list, allow_duplicates=True)

        def add_volume_series(loc: int) -> None:
            """number of shares traded"""
            if DEBUG:
                logger.debug(f"add_volume_series(loc={loc})")
            volume = [int(time_series_dict[i]["5. volume"]) for i in time_series_dict]
            df.insert(loc=loc, column="volume", value=volume, allow_duplicates=True)

        # insert values for each data line into df
        for i, item in enumerate(self.data_line):
            eval(f"add_{item}_series({i})")

        # convert dataframe to list of tuples, tuple name is ticker symbol
        return list(df.itertuples(index=True, name=ticker))


class TiingoDataProcessor(BaseProcessor):
    """Fetch ohlc price data from tiingo.com"""

    from datetime import datetime as dt
    from tiingo import TiingoClient

    def __init__(self, ctx: dict):
        super().__init__(ctx=ctx)
        self.api_key = os.getenv(f"API_TOKEN_{self.data_provider.upper()}")
        self.frequency = ctx["data_service"]["data_frequency"]

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"api_token={self.api_token}, "
            f"frequency={self.frequency}, "
            f"index={self.index}, "
            f"lookback={self.lookback}, "
            f"start_date={self.start_date}, "
        )

    def _tiingo_data_generator(self, ticker: str) -> object:
        """"""
        if DEBUG:
            logger.debug(f"_tiingo_data_generator(ticker={ticker})")

        config = {
            "api_key": self.api_key,
            "session": True,  # reuse the same HTTP Session across API calls
        }
        client = self.TiingoClient(config)

        try:
            historical_prices = client.get_ticker_price(
                ticker=ticker, fmt="json", startDate=self.start_date, endDate=self.end_date, frequency=self.frequency
            )
        except Exception as e:
            logger.debug(f"*** ERROR *** {e}")
        else:
            if not DEBUG:
                print(f" fetching {ticker}...")
            yield ticker, historical_prices

    def _process_tiingo_data(self, data_gen: object) -> list[tuple]:
        """"""
        if DEBUG:
            logger.debug(f"_process_tiingo_data(data_gen={type(data_gen)})")

        ticker, dict_list = next(data_gen)  # unpack items in data_gen

        # create empty dataframe with index as a timestamp
        df = pd.DataFrame(
            index=[round(time.mktime(self.dt.strptime(d["date"][:10], "%Y-%m-%d").timetuple())) for d in dict_list]
        )
        df.index.name = "date"

        # add each data line to dataframe
        def add_clop_series(loc: int) -> None:
            """difference between the close and open price"""
            if DEBUG:
                logger.debug(f"add_clop_series(loc={loc})")
            clop = [round((d["adjClose"] - d["adjOpen"]) * 100) for d in dict_list]
            df.insert(loc=loc, column="clop", value=clop, allow_duplicates=True)

        def add_clv_series(loc: int) -> None:
            """close location value, relative to the high-low range"""
            if DEBUG:
                logger.debug(f"add_clv_series(loc={loc})")
            try:
                clv = [
                    round(((2 * d["adjClose"] - d["adjLow"] - d["adjHigh"]) / (d["adjHigh"] - d["adjLow"])) * 100)
                    for d in dict_list
                ]
                df.insert(loc=loc, column="clv", value=clv, allow_duplicates=True)
            except ZeroDivisionError as e:
                logger.debug(f"*** ERROR *** {e}")

        def add_cwap_series(loc: int) -> None:
            """close weighted average price excluding open price"""
            if DEBUG:
                logger.debug(f"add_cwap_series(loc={loc})")
            cwap = [round(((d["adjHigh"] + d["adjLow"] + 2 * d["adjClose"]) / 4) * 100) for d in dict_list]
            df.insert(loc=loc, column="cwap", value=cwap, allow_duplicates=True)

        def add_hilo_series(loc: int) -> None:
            """difference between the high and low price"""
            if DEBUG:
                logger.debug(f"add_hilo_series(loc={loc})")
            hilo = [round((d["adjHigh"] - d["adjLow"]) * 100) for d in dict_list]
            df.insert(loc=loc, column="hilo", value=hilo, allow_duplicates=True)

        def add_volume_series(loc: int) -> None:
            """number of shares traded"""
            if DEBUG:
                logger.debug(f"add_volume_series(loc={loc})")
            volume = [d["adjVolume"] for d in dict_list]
            df.insert(loc=loc, column="volume", value=volume, allow_duplicates=True)

        # insert values from each data line into df
        for i, item in enumerate(self.data_line):
            eval(f"add_{item}_series({i})")

        # convert dataframe to list of tuples, tuple name is ticker symbol
        return list(df.itertuples(index=True, name=ticker))


class YahooFinanceDataProcessor(BaseProcessor):
    """Fetch ohlc price data from tiingo.com"""

    import yfinance as yf

    def __init__(self, ctx: dict):
        super().__init__(ctx=ctx)
        self.interval = self._parse_frequency

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"data_line={self.data_line}, "
            f"data_provider={self.data_provider}, "
            f"index={self.index}, "
            f"interval={self.interval}, "
            f"start_date={self.start_date}, "
            f"end_date={self.end_date})"
        )

    @property
    def _parse_frequency(self):
        """Convert daily/weekly frequency to provider format"""
        frequency_dict = {"daily": "1d", "weekly": "1w"}
        return frequency_dict[self.frequency]

    def _yfinance_data_generator(self, ticker: str) -> object:
        """"""
        if DEBUG:
            logger.debug(f"_yfinance_data_generator(index={self.index}, ticker={ticker})")

        try:
            yf_ticker = self.yf.Ticker(ticker=ticker)
            df = yf_ticker.history(start=self.start_date, end=self.end_date, interval=self.interval)
        except Exception as e:
            logger.debug(f"*** ERROR *** {e}")
        else:
            if not DEBUG:
                print(f" fetching {ticker}...")
            yield self.ticker, df

    def _process_yfinance_data(self, data_gen: object) -> list[tuple]:
        """"""
        if DEBUG:
            logger.debug(f"_process_yfinance_data(data_gen={type(data_gen)}, data_line={type(self.data_line)})")

        ticker, yf_df = next(data_gen)

        # create empty dataframe with index as a timestamp
        df = pd.DataFrame(index=yf_df.index.values.astype(int) // 10**9)
        df.index.name = "date"

        # add each data line to dataframe
        def add_clop_series(loc: int) -> None:
            """difference between the close and open price"""
            if DEBUG:
                logger.debug(f"add_clop_series(loc={loc})")

            df.insert(
                loc=loc,
                column="clop",
                value=list(round((yf_df["Close"] - yf_df["Open"]) * 100).astype(int)),
                allow_duplicates=True,
            )

        def add_clv_series(loc: int) -> None:
            """close location value, relative to the high-low range"""
            if DEBUG:
                logger.debug(f"add_clv_series(loc={loc})")
            try:
                clv = list(
                    round((2 * yf_df["Close"] - yf_df["Low"] - yf_df["High"]) / (yf_df["High"] - yf_df["Low"]) * 100)
                )
            except ZeroDivisionError as e:
                logger.debug(f"*** ERROR *** {e}")
            else:
                df.insert(loc=loc, column="clv", value=clv, allow_duplicates=True)

        def add_cwap_series(loc: int) -> None:
            """close weighted average price excluding open price"""
            if DEBUG:
                logger.debug(f"add_cwap_series(loc={loc})")

            df.insert(
                loc=loc,
                column="cwap",
                value=list(round((yf_df["High"] + yf_df["Low"] + 2 * yf_df["Close"]) / 4 * 100).astype(int)),
                allow_duplicates=True,
            )

        def add_hilo_series(loc: int) -> None:
            """difference between the high and low price"""
            if DEBUG:
                logger.debug(f"add_hilo_series(loc={loc})")

            df.insert(
                loc=loc,
                column="hilo",
                value=list(round((yf_df["High"] - yf_df["Low"]) * 100).astype(int)),
                allow_duplicates=True,
            )

        def add_volume_series(loc: int) -> None:
            """number of shares traded"""
            if DEBUG:
                logger.debug(f"add_volume_series(loc={loc})")
            df.insert(loc=loc, column="volume", value=list(yf_df["Volume"]), allow_duplicates=True)

        # insert values for each data line into df
        for i, item in enumerate(self.data_line):
            eval(f"add_{item}_series({i})")

        # convert dataframe to list of tuples, tuple name is ticker symbol
        return list(df.itertuples(index=True, name=ticker))
