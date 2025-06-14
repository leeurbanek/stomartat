# python -m unittest test/test_data_srv/test_client.py -v
import unittest
from unittest.mock import Mock

from pkg.data_srv import client
from test import data


@unittest.skip(reason='ok')
class TestDataImport(unittest.TestCase):

    def test_ctx_alphavantage(self):
        assert isinstance(data.ctx_alphavantage, dict)

    def test_ctx_tiingo_dict(self):
        assert isinstance(data.ctx_tiingo, dict)

    def test_ctx_yf_dict(self):
        assert isinstance(data.ctx_yfinance, dict)


# @unittest.skip(reason='ok')
class TestAlphaVantageReader(unittest.TestCase):

    def test_select_data_provider_alphavantage(self, ):
        result = client._select_data_provider(ctx=data.ctx_alphavantage, symbol="IWM")
        print(f" _select_data_provider_alphavantage(), {result}")

# class MyClass:
#     def my_method(self):
#         return "Hello, World!"

# class TestMyClass(unittest.TestCase):
#     def test_my_method(self):
#         my_class = MyClass()
#         my_class.my_method = Mock(return_value="Mocked method")

#         result = my_class.my_method()

#         self.assertEqual(result, "Mocked method")


if __name__ == '__main__':
    unittest.main()
