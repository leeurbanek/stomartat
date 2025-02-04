import logging

from pathlib import Path
from configparser import ConfigParser

from src import config_file

# Select which version of the webscraper to use
from src.chart_service.scraper.my_requests import WebScraper
# from src.chart_service.scraper.my_selenium import WebScraper


conf_obj = ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
conf_obj.read(config_file)

logger = logging.getLogger(__name__)


def get_chart(ctx):
    """"""
    debug = ctx['debug']
    period = ctx['period']
    symbol = ctx['symbol']

    # check 'chart' folder exists in users 'work_dir', if not create 'chart' folder
    Path(f"{conf_obj.get('Default', 'work_dir')}/chart").mkdir(parents=True, exist_ok=True)

    if debug: logger.debug(f"get_chart(ctx={ctx})")
    if not debug: print('Begin download')

    # count = len(period) * len(symbol)
    [download(debug, p, s.strip(',')) for p in period for s in symbol]
    if not debug: print('cleaning up... ', end='')
    if not debug: print('\b finished!')
    if not debug: print(f"Saved charts to '{conf_obj.get('Default', 'work_dir')}/chart'.")


def download(debug, period, symbol):
    """"""
    if debug: logger.debug(f"download(period={period} {type(period)}, symbol={symbol} {type(symbol)})")

    start = WebScraper(debug, period, symbol)
    try:
        start.webscraper()
    except:
        pass
