# python -m unittest test/test_data_srv/test_reader.py -v
import unittest
from datetime import date
from unittest.mock import Mock

import pandas as pd

from pkg.data_srv import reader
from test import data


@unittest.skip(reason='ok')
class TestDataImport(unittest.TestCase):

    def test_ctx_alphavantage(self):
        assert isinstance(data.ctx_alphavantage, dict)

    def test_ctx_tiingo_dict(self):
        assert isinstance(data.ctx_tiingo, dict)

    def test_ctx_yf_dict(self):
        assert isinstance(data.ctx_yfinance, dict)


@unittest.skip(reason='ok')
class TestAlphaVantageReader(unittest.TestCase):

    def setUp(self):
        self.reader = reader.AlphaVantageReader(ctx=data.ctx_alphavantage)
        self.reader.start_date = date.fromisoformat("2025-05-21")
        self.reader._fetch_ohlc_price_data = Mock(return_value=data.raw_alphavantage)

    def test_instance(self):
        assert isinstance(self.reader, reader.AlphaVantageReader)
        print(f" {self.reader}")

    def test_fetch_ohlc_price_data(self):
        result = self.reader._fetch_ohlc_price_data('IWM')
        self.assertEqual(result, data.raw_alphavantage)

    def test_parse_price_data(self):
        result = self.reader._parse_price_data(data.raw_alphavantage)
        print(f" alphavantage_parse_price_data(), {result}")
        self.assertEqual(result, data.parsed_alphavantage)

    def test_create_dataframe(self):
        result = self.reader._create_dataframe(parsed_data=data.parsed_alphavantage)
        # print(f" alphavantage_create_dataframe(), {result}")
        self.assertIsInstance(result, pd.DataFrame)

    def test_get_ticker_df_tuple(self):
        result = self.reader.get_ticker_df_tuple('IWM')
        print(f" alphavantage get_ticker_df_tuple(), {result}")


@unittest.skip(reason='ok')
class TiingoReaderTest(unittest.TestCase):

    def setUp(self):
        self.reader = reader.TiingoReader(ctx=data.ctx_tiingo)
        self.reader._fetch_ohlc_price_data = Mock(return_value=data.raw_tiingo)

    def test_instance(self):
        assert isinstance(self.reader, reader.TiingoReader)
        print(f" {self.reader}")

    def test_fetch_ohlc_price_data(self):
        result = self.reader._fetch_ohlc_price_data('IWM')
        self.assertEqual(result, data.raw_tiingo)

    def test_parse_price_data(self):
        result = self.reader._parse_price_data(data.raw_tiingo)
        # print(f" tiingo_parse_price_data(), {result}")
        self.assertEqual(result, data.parsed_tiingo)

    def test_create_dataframe(self):
        result = self.reader._create_dataframe(parsed_data=data.parsed_tiingo)
        # print(f" tiingo_create_dataframe(), {result}")
        self.assertIsInstance(result, pd.DataFrame)

    def test_get_ticker_df_tuple(self):
        result = self.reader.get_ticker_df_tuple('IWM')
        print(f" tiingo get_ticker_df_tuple(), {result}")


# @unittest.skip(reason='ok')
class YahooFinanceReaderTest(unittest.TestCase):

    def setUp(self):
        self.reader = reader.YahooFinanceReader(ctx=data.ctx_yfinance)
        self.reader._fetch_ohlc_price_data = Mock(return_value=data.raw_yfinance)

    def test_instance(self):
        assert isinstance(self.reader, reader.YahooFinanceReader)
        print(f" {self.reader}")

    def test_fetch_ohlc_price_data(self):
        result = self.reader._fetch_ohlc_price_data('IWM')
        self.assertEqual(result, data.raw_yfinance)

    def test_parse_price_data(self):
        result = self.reader._parse_price_data(data.raw_yfinance)
        print(f" yfinance_parse_price_data(), {result}")
        self.assertEqual(result, data.parsed_yfinance)

    def test_create_dataframe(self):
        result = self.reader._create_dataframe(parsed_data=data.parsed_yfinance)
        # print(f" yfinance_create_dataframe(), {result}")
        self.assertIsInstance(result, pd.DataFrame)

    def test_get_ticker_df_tuple(self):
        result = self.reader.get_ticker_df_tuple('IWM')
        print(f" yfinance get_ticker_df_tuple(), {result}")


if __name__ == '__main__':
    unittest.main()
