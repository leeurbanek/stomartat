"""src/pkg/config_srv/scraper.py\n
def update_scraper(ctx)"""
import logging


logger = logging.getLogger(__name__)


def update_scraper(ctx):
    """"""
    """"""
    if ctx.obj['default']['debug']:
        logger.debug(f"update_scraper(ctx={ctx.obj}")

    # Get first item in arguments tuple
    new_value = ctx.obj['interface']['arguments'][0]
    return new_value
