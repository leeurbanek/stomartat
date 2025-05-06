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

    # Add 'arguments' to 'interface' ctx
    if arguments:  # use symbols in arguments list
        ctx['interface']['arguments'] = sorted([i.upper() for i in list(arguments)])
    else:  # use data_service chart_list
        ctx['interface']['arguments'] = sorted(list(ctx['data_service']['data_list'].split(' ')))

    if DEBUG: logger.debug(f"cli(ctx={ctx} {type(ctx)}, arguments={arguments})")

    if click.confirm(f" Downloading: {ctx['interface']['arguments']}\n Do you want to continue?"):
        # Download data
        from pkg.data_srv import client
        client.get_ohlc_data(ctx=ctx)
    else:  # Print default message
        click.echo(" Goodby.")
