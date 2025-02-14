"""src/pkg/chart_srv/client.py"""
import logging

from pathlib import Path


logger = logging.getLogger(__name__)


def get_chart(ctx):
    """"""
    DEBUG = ctx.obj['default']['debug']
    if DEBUG: logger.debug(f"get_chart(ctx={ctx.obj})")

    # check 'chart' folder exists in users 'work_dir', if not create 'chart' folder
    Path(f"{ctx.obj['default']['work_dir']}/chart").mkdir(parents=True, exist_ok=True)

    if not DEBUG: print('Begin download')
    [download(ctx, p, s.strip(',')) for p in ctx.obj['interface']['opt_trans'] for s in ctx.obj['interface']['arguments']]
    if not DEBUG: print('cleaning up... ', end='')
    if not DEBUG: print('\b finished!')
    if not DEBUG: print(f"Saved charts to '{ctx.obj['default']['work_dir']}chart'.")


def download(ctx, period, symbol):
    """"""
    if ctx.obj['default']['debug']:
        logger.debug(f"download(period={period} {type(period)}, symbol={symbol} {type(symbol)})")

    # Select which version of the webscraper to use
    if ctx.obj['chart_service']['scraper'] == 'requests':
        from pkg.chart_srv.scraper.my_requests import WebScraper
    elif ctx.obj['chart_service']['scraper'] == 'selenium':
        from pkg.chart_srv.scraper.my_selenium import WebScraper

    start = WebScraper(ctx, period, symbol)
    try:
        start.webscraper()
    except Exception as e:
        print(e)
