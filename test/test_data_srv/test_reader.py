# python -m unittest test/test_data_srv/test_reader.py -v
import unittest

from pkg.data_srv.reader import TiingoReader
from test.data import ctx, dict_list_iwm


# @unittest.skip(reason=None)
class TestDataImport(unittest.TestCase):

    def test_ctx_dict(self):
        assert isinstance(ctx, dict)


# @unittest.skip(reason=None)
class TiingoReaderTest(unittest.TestCase):

    def setUp(self):
        self.tiingo = TiingoReader(ctx=ctx)

    def test_instance(self):
        # tiingo = TiingoReader(ctx=ctx)
        assert isinstance(self.tiingo, TiingoReader)

    def test_fetch_ohlc_price_data(self):
        pass



# class MySeleniumTest(unittest.TestCase):
#     def setUp(self):
#         self.base_url = ctx['chart_service']['base_url']

#     def test_webscraper(self):
#         my_selenium.WebScraper(ctx=ctx).webscraper()


if __name__ == '__main__':
    unittest.main()
