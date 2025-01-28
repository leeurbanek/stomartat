"""src/pkg/config_srv/ticker_symbol.py\n
def cli_update(ctx)"""
import logging


logger = logging.getLogger(__name__)


def cli_update(ctx):
    """"""
    if ctx.obj['default']['debug']:
        logger.debug(f"cli_update(ctx={ctx.obj})")

    # Lists of current and argument symbols
    cur_sym = ctx.obj['chart_service']['symbol'].split(' ')
    arg_sym = list(ctx.obj['cli']['arguments'])

    extend_list, remove_list = [], []  # create lists

    # Add symbols to extend_list/remove_list
    for item in arg_sym:
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
    new_value = ', '.join(cur_sym)
    return new_value
