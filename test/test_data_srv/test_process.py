# python -m unittest test/test_data_srv/test_client.py -v
import unittest
from datetime import date
from unittest.mock import Mock

import pandas as pd

from pkg.data_srv import process
from test import data


# @unittest.skip(reason='ok')
class TestDataImport(unittest.TestCase):

    def test_ctx_alphavantage(self):
        assert isinstance(data.ctx_alphavantage, dict)

    def test_ctx_tiingo_dict(self):
        assert isinstance(data.ctx_tiingo, dict)

    def test_ctx_yf_dict(self):
        assert isinstance(data.ctx_yfinance, dict)


# # @unittest.skip(reason='wip')
# class TestAlphaVantageReader(unittest.TestCase):

#     def setUp(self):
#         self.reader = reader.AlphaVantageReader(ctx=data.ctx_alphavantage)
#         self.reader.start_date = date.fromisoformat("2025-05-21")
#         self.reader._fetch_ohlc_price_data = Mock(return_value=data.raw_alphavantage)

#     def test_instance(self):
#         assert isinstance(self.reader, reader.AlphaVantageReader)
#         print(f" {self.reader}")

#     def test_fetch_ohlc_price_data(self):
#         result = self.reader._fetch_ohlc_price_data('IWM')
#         self.assertEqual(result, data.raw_alphavantage)

#     def test_parse_price_data(self):
#         result = self.reader._parse_price_data(data.raw_alphavantage)
#         print(f" alphavantage_parse_price_data(), {result}")
#         self.assertEqual(result, data.parsed_alphavantage)


if __name__ == '__main__':
    unittest.main()
