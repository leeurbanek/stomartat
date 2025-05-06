"""src/pkg/chart_srv/client.py\n
get_stockchart(ctx) - fetch OHLC charts\n
get_heatmap(ctx) - fetch S&P 500 heatmaps
"""
import logging

from pathlib import Path

from pkg import DEBUG


logger = logging.getLogger(__name__)


# TODO combine get_heatmap and get_stockchart
def get_heatmap(ctx):
    """Check if `heatmap` folder exists. Direct workflow of client"""
    if DEBUG: logger.debug(f"get_heatmap(ctx={type(ctx)})")

    # check 'heatmap' folder exists in users 'work_dir', if not create 'heatmap' folder
    Path(f"{ctx['default']['work_dir']}/heatmap").mkdir(parents=True, exist_ok=True)

    if not DEBUG: print('\nBegin download')
    _download(ctx=ctx)

    if not DEBUG: print(' finished!')
    if not DEBUG: print(f"Saved heatmaps to:\n'{ctx['default']['work_dir']}heatmap'\n")


def get_stockchart(ctx):
    """Check if `chart` folder exists. Direct workflow of client"""
    if DEBUG: logger.debug(f"get_stockchart(ctx={type(ctx)})")

    # check 'chart' folder exists in users 'work_dir', if not create 'chart' folder
    Path(f"{ctx['default']['work_dir']}/chart").mkdir(parents=True, exist_ok=True)

    if not DEBUG: print('\nBegin download')
    _download(ctx=ctx)

    if not DEBUG: print(' finished!')
    if not DEBUG: print(f"Saved charts to:\n'{ctx['default']['work_dir']}chart'\n")


def _download(ctx):
    """"""
    if DEBUG: logger.debug(f"_download(ctx={type(ctx)})")

    # Select which version of the webscraper to use
    if ctx['interface']['command'] == 'chart':
        from pkg.chart_srv.scraper.stock_chart import WebScraper
    elif ctx['interface']['command'] == 'heatmap':
        from pkg.chart_srv.scraper.heat_map import WebScraper

    start = WebScraper(ctx)
    try:
        start.webscraper()
    except Exception as e:
        print(e)
