"""src/pkg/cli/cmd_data.py"""
import logging

import click

from pkg import DEBUG


logger = logging.getLogger(__name__)

@click.command('data', short_help="Fetch online stockmarket data", help=
"""
\b
NAME
    data - Fetch online stockmarket data
\b
DESCRIPTION
    The data utility fetches historical ohlc stock price data.
    Downloaded data is saved to the work directory. If no ticker
    symbols (arguments) are provided the default symbol list is used.
""")

@click.argument(
    'arguments', nargs=-1, default=None, required=False, type=str
)

# @click.pass_context
@click.pass_obj
def cli(ctx, arguments):
    """Run data command"""
    ctx['interface']['command'] = 'data'

    # add arguments to interface ctx and set database name
    if arguments:  # use symbols in arguments list
        ctx['interface']['arguments'] = sorted([i.upper() for i in list(arguments)])
        ctx['interface']['database'] = click.prompt(
            f" Using database `custom.db`.\n Type a new database name to change,\n press Enter to accept.", default="custom.db"
        )
    else:  # use symbols in data_service data_list
        ctx['interface']['arguments'] = sorted(list(ctx['data_service']['data_list'].split(' ')))
        ctx['interface']['database'] = click.prompt(
            f" Using database `default.db`.\n Type a new database name to change,\n press Enter to accept", default="default.db"
        )

    if click.confirm(f" Saving data for {ctx['interface']['arguments']} to `{ctx['interface']['database']}`.\n Do you want to continue?"):
        # download data
        from pkg.data_srv import client
        if DEBUG: logger.debug(
            f"cli(ctx={type(ctx)}, arguments={ctx['interface']['arguments']})"
        )
        for symbol in ctx['interface']['arguments']:
            client.get_ohlc_data(ctx=ctx, symbol=symbol)
