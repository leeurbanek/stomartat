"""src/pkg/setting/ticker_symbol.py"""
import logging
# import os

import click

# from pkg import config_obj
# print(f"config_obj: {dict(config_obj.items('Ticker'))}")
# print(f"config_obj: {config_obj.get('Ticker', 'symbol')}")

# config_items = config_obj.items('section_name')
# config_dict = {key: value for key, value in config_items}
# print(f"config_dict: {config_dict}")

# conf_obj.read(config_file)

logger = logging.getLogger(__name__)


def update_ts(ctx):
    """"""
    if ctx.obj['default']['debug']:
         logger.debug(f"update_ts(ctx={ctx.obj})")


    # current = f"{conf_obj.get('Ticker', 'symbol')}"
    # click.echo(f"Current {ctx_obj['opt_trans']}: '{current}'\nTry 'markdata config --help' for help.")

    # # Current ticker symbols from config.ini
    # conf_symbol = conf_obj.getlist('Ticker', 'symbol')
    # # ctx_obj symbols from command line arquments
    # ctx_symbol = ctx_obj['symbol']

    # extend, remove = [], []  # create lists

    # # Add symbols to extend/remove list
    # for s in ctx_symbol:
    #     s = s.upper().strip()
    #     if s in conf_symbol:
    #         remove.append(s)
    #     else:
    #         extend.append(s.strip())

    # # Extend/remove items in symbol_list
    # if extend:
    #     click.confirm(
    #         f"Adding symbols: {', '.join(extend)}\nDo you want to continue?", abort=True
    #         )
    #     conf_symbol.extend(extend)
    # if remove:
    #     click.confirm(
    #         f"Removing symbols: {', '.join(remove)}\nDo you want to continue?", abort=True
    #         )
    #     for r in remove:
    #         conf_symbol.remove(r)

    # # Convert symbol_list to new_value string
    # new_value = ', '.join(conf_symbol)
    # return new_value
