"""src/pkg/chart_srv/scraper/my_requests.py\n
Use urllib3 to get charts with the saved chart_url in the
chart_cfg.ini file then save to work directory. The Pillow
module is used to convert byte data to a png image. The urls
used are hard coded in pkg/chart_srv/cfg_chart.ini variables.
"""
import io, os
import logging, logging.config

# from time import time as epoch_time
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import urllib3

from PIL import Image


logging.config.fileConfig(fname='src/logger.ini')
logging.getLogger('PIL').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class WebScraper:
    """Fetch and save SharpCharts from stockcharts.com"""
    def __init__(self, ctx):
        self.chart_dir = f"{ctx['default']['work_dir']}chart"
        self.debug = ctx['default']['debug']
        self.http = urllib3.PoolManager()
        self.period = ctx['interface']['opt_trans']
        self.symbol = ctx['interface']['arguments']
        try:
            if ctx['chart_service']['chart_skin'] == 'dark':
                self.url = ctx['chart_service']['chart_dark']
            elif ctx['chart_service']['chart_skin'] == 'light':
                self.url = ctx['chart_service']['chart_light']
        except Exception as e:
            print(e)

    def __repr__(self):
        return f"<class '{self.__class__.__name__}'> __dict__= {self.__dict__})"

    def webscraper(self):
        """Main entry point to Webscraper class. Directs workflow
        of webscraper.
        """
        if self.debug: logger.debug(f'webscraper({self} {type(self)})')
        if not self.debug: print(' Fetching chart:')

        for symbol in self.symbol:
            for period in self.period:
                mod_url = self._modify_query_period_and_symbol(period=period, symbol=symbol)
                self._get_img_src_convert_bytes_to_png_and_save(mod_url=mod_url, period=period, symbol=symbol)

    def _modify_query_period_and_symbol(self, period: str, symbol: str):
        """Use urllib.parse to modify the default query parameters
        with new period, symbol.
        """
        if self.debug: logger.debug(f'_modify_query_period_and_symbol(period={period} {type(period)}, symbol={symbol} {type(symbol)})')

        parsed_url = urlparse(url=self.url)
        query_dict = parse_qs(parsed_url.query)
        if period != 'Daily':
            query_dict['p'] = period[0]
            query_dict['yr'] = '5'
        query_dict['s'] = symbol
        # query_dict['r'] = str(round(epoch_time() * 1000))
        encoded_params = urlencode(query_dict, doseq=True)
        return urlunparse(parsed_url._replace(query=encoded_params))

    def _get_img_src_convert_bytes_to_png_and_save(self, mod_url: str, period: str, symbol: str):
        """Get the chart image source and convert the bytes to
        a .png image then save to the chart work directory.
        """
        if self.debug: logger.debug(f'_get_img_src_convert_bytes_to_png_and_save(mod_url={mod_url} {type(mod_url)})')
        if not self.debug: print(f'   {symbol} {period.lower()}... ')

        image_src = self.http.request('GET', mod_url, headers={'User-agent': 'Mozilla/5.0'})
        image = Image.open(io.BytesIO(image_src.data)).convert('RGB')
        image.save(os.path.join(self.chart_dir, f'{symbol}_{period[:1].lower()}.png'), 'PNG', quality=80)
