"""src/pkg/chart_srv/client.py"""
import logging

from pathlib import Path


logger = logging.getLogger(__name__)


def get_chart(ctx):
    """Check if `chart` folder exists. Direct workflow of client"""
    DEBUG = ctx['default']['debug']
    if DEBUG: logger.debug(f"get_chart(ctx={type(ctx)})")

    # check 'chart' folder exists in users 'work_dir', if not create 'chart' folder
    Path(f"{ctx['default']['work_dir']}/chart").mkdir(parents=True, exist_ok=True)

    if not DEBUG: print('\nBegin download')
    _download(ctx=ctx)

    if not DEBUG: print(' finished!')
    if not DEBUG: print(f"Saved charts to:\n'{ctx['default']['work_dir']}chart'\n")


def _download(ctx):
    """"""
    if ctx['default']['debug']: logger.debug(f"_download(ctx={type(ctx)})")

    # Select which version of the webscraper to use
    if ctx['chart_service']['scraper'] == 'requests':
        from pkg.chart_srv.scraper.my_requests import WebScraper
    elif ctx['chart_service']['scraper'] == 'selenium':
        from pkg.chart_srv.scraper.my_selenium import WebScraper

    start = WebScraper(ctx)
    try:
        start.webscraper()
    except Exception as e:
        print(e)
