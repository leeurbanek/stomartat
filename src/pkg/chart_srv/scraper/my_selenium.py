"""src/pkg/chart_srv/scraper/my_selenium.py\n
Use Selenium Firefox webdriver to scrape chart url from base
url, then use urllib3 to get charts and save to work directory.
The Pillow module is used to convert byte data to a png image.
"""
import logging, logging.config

import colorlog

from pkg.ctx_mgr import WebDriverManager


logging.config.fileConfig(fname='src/logger.ini')
logging.getLogger('PIL').setLevel(logging.WARNING)
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = colorlog.getLogger(__name__)


class WebScraper:
    """Fetch and save SharpCharts from stockcharts.com"""
    def __init__(self, ctx):
        self.base_url = ctx['chart_service']['base_url']
        self.chart_url = ctx['chart_service']['chart_url']
        self.chart_dir = f"{ctx['default']['work_dir']}/chart"
        self.ctx = ctx
        self.debug = ctx['default']['debug']
        self.period = ctx['interface']['opt_trans']
        self.symbol = ctx['interface']['arguments']

    def __repr__(self):
        return f'{self.__class__.__name__}(ctx={self.ctx})'

    def webscraper(self):
        """Main entry point to Webscraper class. Directs workflow
        of webscraper.
        """
        with WebDriverManager(debug=self.debug) as driver:
            if self.debug: logger.debug(f'webscraper(self={self}, driver={driver})')
            # chart_url = self._fetch_stock_chart_url(driver=driver)
            chart_url = self.chart_url
            self._get_img_src_convert_bytes_to_png_and_save(chart_url=chart_url)

    def _fetch_stock_chart_url(self, driver: object):
        """Return the stock chart url with todays timestamp.
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        if self.debug: logger.debug(f'_fetch_stock_chart_url(self={type(self)}, driver={type(driver)})')

        driver.get(self.base_url)
        WebDriverWait(driver, 7).until(
            # EC.presence_of_all_elements_located((By.ID, "chart-settings-mode-ui"))
            EC.presence_of_all_elements_located((By.ID, "chart-image"))
        )
        return driver.find_element(By.XPATH, "//div/img").get_attribute("src")

    def _get_img_src_convert_bytes_to_png_and_save(self, chart_url: str):
        """For each period in the `ctx interface opt_trans` dictionary
        get the chart for each symbol in the `ctx interface arguments`
        list. Convert the bytes to a .png image then save to the chart
        work directory.
        """
        import io, os
        import urllib3
        from PIL import Image

        if self.debug: logger.debug(f'_get_img_src_convert_bytes_to_png_and_save(chart_url {type(chart_url)})')

        http = urllib3.PoolManager()
        # Update the default url with our symbol and period
        for period in self.period:
            for symbol in self.symbol:
                new_url = self._replace_period_symbol_in_chart_url(chart_url, period, symbol)
                if self.debug: logger.debug(f'_replace_period_symbol_in_chart_url({new_url}, {period}, {symbol})')

                # Get the chart image source convert to .png and save
                image_src = http.request('GET', new_url, headers={'User-agent': 'Mozilla/5.0'})
                image = Image.open(io.BytesIO(image_src.data)).convert('RGB')
                image.save(os.path.join(self.chart_dir, f'{symbol}_{period[:1].lower()}.png'), 'PNG', quality=80)

    def _replace_period_symbol_in_chart_url(self, chart_url: str, period: str, symbol: str):
        """"""
        import time

        if period != 'Daily':
            chart_url = chart_url.replace('p=D', 'p=W').replace('yr=1', 'yr=5')
        new_url = chart_url.replace('AAPL', symbol)
        # Return new_url with current epoch time parsed in.
        return new_url[:-13]+str(round(time.time() * 1000))


if __name__ == '__main__':
    from test import data

    # start = WebScraper(ctx=data.ctx_default)
    # start.webscraper()

    start = WebScraper(ctx=data.ctx_custom)
    start.webscraper()

# ===

# # import io
# import logging
# # import os
# # from configparser import ConfigParser

# # import requests
# from bs4 import BeautifulSoup
# # from PIL import Image
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import Select

# # from src import config_file
# from pkg import ctx_mgr

# # conf_obj = ConfigParser()
# # conf_obj.read(config_file)

# logging.getLogger('PIL').setLevel(logging.WARNING)
# logging.getLogger('selenium').setLevel(logging.WARNING)
# logging.getLogger('urllib3').setLevel(logging.WARNING)
# logger = logging.getLogger(__name__)
# logger.debug(f"my_selenium())")

# # BASE_URL = conf_obj['Scraper']['base_url']
# # CHART_DIR = f"{conf_obj['Default']['work_dir']}/chart"

# class WebScraper:
#     """"""
#     from selenium.webdriver.support.ui import Select

#     def __init__(self, ctx, period, symbol) -> None:
#         # self.base_url = ctx.obj['chart_service']['base_url']
#         self.chart_dir = f"{ctx.obj['default']['work_dir']}chart"
#         self.debug = ctx.obj['default']['debug']
#         self.period = period
#         self.symbol = symbol
#         self.url = ctx.obj['chart_service']['base_url']+symbol

#     def __repr__(self) -> str:
#         return f"{self.__class__.__name__}(debug={self.debug}{type(self.debug)}, symbol={self.symbol}{type(self.symbol)} period={self.period}{type(self.period)})"

#     def webscraper(self):
#         """"""
#         if self.debug: logger.debug(f'webscraper({self.symbol}, {self.period})')
#         with ctx_mgr.WebDriverManager(debug=self.debug) as driver:
#             if not self.debug: print(f'  fetching chart: {self.symbol}_{self.period.lower()}.png... ', end=' ')
#             with ctx_mgr.SpinnerManager(debug=self.debug):
#                 self._set_chart_page(driver)
#                 content = self._get_page_content(driver)
# #                 src = self._get_img_src(content)
# #                 self._save_img_to_file(src)
# #             if not self.debug: print('\b done,')

#     def _get_img_src(self, soup=None):
#         """"""
#         if self.debug: logger.debug(f'_get_img_src(soup: {type(soup)})')
# #         attr = soup.find(attrs={'class': "chartnotes-container"})
# #         img = attr.find("img")
# #         return img.get("src")

#     def _get_page_content(self, driver):
#         """"""
#         driver.implicitly_wait(3)
#         content = driver.page_source
#         if self.debug: logger.debug(f'_get_page_content({content})')
#         return BeautifulSoup(content, features='html.parser')

#     def _save_img_to_file(self, src=None):
#         """"""
#         if self.debug: logger.debug(f'_save_img_to_file({type(src)})')

# #         src_content = requests.get(f'https:{src}', headers={'User-agent': 'Mozilla/5.0'}).content

# #         image_file = io.BytesIO(src_content)
# #         image = Image.open(image_file).convert('RGB')
# #         image.save(os.path.join(CHART_DIR, f'{self.symbol}_{self.period.lower()}.png'), 'PNG', quality=80)

#     def _set_chart_page(self, driver):
#         """"""
#         if self.debug: logger.debug(f'scraper_obj._set_chart_page({self.symbol}, {self.period})')
#         year = 1  # for setting dataRange predef field
#         if self.period == 'Weekly': year = 5

#         driver.get(f'{self.url}')
#         driver.implicitly_wait(3)

#         # period2 = Select(driver.find_element(By.ID, 'period2'))
#         # period2.select_by_visible_text(f'{self.period}')

#         # dataRange = Select(driver.find_element(By.ID, 'dataRange'))
#         # dataRange.select_by_value(f'predef:{year}|0|0')

#         # chartSize = Select(driver.find_element(By.ID, 'chartSize'))
#         # chartSize.select_by_visible_text('Landscape')

#         # chartSkin = Select(driver.find_element(By.ID, 'chartSkin'))
#         # chartSkin.select_by_visible_text('night')

#         # driver.find_element(By.XPATH, '//input[@type="button"][@value="Update"]').click()


# # # WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, 'Element's XPath')))
