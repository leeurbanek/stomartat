"""src/pkg/config_srv/chart.py\n
update_chart_list(ctx)\n
update_chart_skin(ctx)\n
update_scraper(ctx)
"""
import logging


logger = logging.getLogger(__name__)


def update_chart_list(ctx: dict):
    """Set the default list of chart symbols to download."""
    # Lists of current and argument symbols
    arguments = list(ctx['interface']['arguments'])
    cur_sym = ctx['chart_service']['chart_list'].split(' ')

    if ctx['default']['debug']:
        logger.debug(f"update_chart_list(ctx={ctx}, {type(ctx)})")

    extend_list, remove_list = [], []  # create lists

    # Add symbols to extend_list/remove_list
    for item in arguments:
        item = item.upper().strip()

        if item in cur_sym:
            remove_list.append(item)
        else:
            extend_list.append(item)

    # Extend/remove items in symbol_list
    if extend_list:
        cur_sym.extend(extend_list)
    if remove_list:
        for r in remove_list:
            cur_sym.remove(r)

    # Convert symbol list to string
    new_value = ', '.join(cur_sym).replace(',', '')
    return new_value


def update_chart_skin(ctx: dict):
    """Change the chart appearance: light/dark."""
    if ctx['default']['debug']:
        logger.debug(f"update_chart_skin(ctx={ctx}, {type(ctx)})")

    return ctx['interface']['arguments'][0]


def update_scraper(ctx: dict):
    """Use Selenium or urllib3 for chart webscraper."""
    if ctx['default']['debug']:
        logger.debug(f"update_scraper(ctx={ctx}, {type(ctx)}")

    # Get first item in arguments tuple
    new_value = ctx['interface']['arguments'][0]
    return new_value
