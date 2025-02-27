"""src/pkg/config_srv/chart.py
update_chart_skin(ctx)
update_scraper(ctx)
update_chart_list(ctx)"""
import logging


logger = logging.getLogger(__name__)


def update_chart_skin(ctx):
    """"""
    if ctx.obj['default']['debug']:
        logger.debug(f"update_chart_skin(ctx={ctx.obj})")

    return ctx.obj['interface']['arguments'][0]


def update_scraper(ctx):
    """"""
    if ctx.obj['default']['debug']:
        logger.debug(f"update_scraper(ctx={ctx.obj}")

    # Get first item in arguments tuple
    new_value = ctx.obj['interface']['arguments'][0]
    return new_value


def update_chart_list(ctx):
    """"""
    # Lists of current and argument symbols
    arguments = list(ctx.obj['interface']['arguments'])
    cur_sym = ctx.obj['chart_service']['chart_list'].split(' ')

    if ctx.obj['default']['debug']:
        logger.debug(f"update_chart_list(ctx={ctx.obj})")

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
