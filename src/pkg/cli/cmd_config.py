"""src/pkg/cli/cmd_config.py"""
import logging

import click

logger = logging.getLogger(__name__)


@click.command('config', short_help="Edit configuration settings", help=
"""
\b
NAME
    config -- Change configuration settings
\b
SYNOPSIS
    config [Options] [argument1 argument2 ...]
\b
DESCRIPTION
    The config utility writes any specified arguments, separated
    by single blank (' ') characters, to the config.ini file.
    Use absolute paths for directories, etc.  Quotes are not needed.
""")

# config ticker symbol
@click.option(
    '--symbol', 'opt_trans', flag_value='symbol',
    help=f"Add/remove ticker symbols, current: "
)
@click.pass_context
def cli(ctx, opt_trans):
    """Run config command"""
    # Add 'opt_trans' to ctx
    ctx.obj['cli']['opt_trans'] = opt_trans

    if ctx.obj['default']['debug']: 
        logger.debug(f"cli(ctx={ctx.obj}, opt_trans={opt_trans})")

    if opt_trans == 'symbol':
        from pkg.setting import ticker_symbol
        ticker_symbol.update_ts(ctx)

    # elif opt_trans == 'symbol':
    #     section = conf_obj['Ticker']
    #     ctx.obj['section'] = section  # add section to ctx
    #     ctx.obj['symbol'] = arguments
    #     new_value = update_ticker_symbol(conf_obj, ctx.obj)
    #     if new_value:
    #         section[opt_trans] = new_value
    #         write_new_value_to_config()
