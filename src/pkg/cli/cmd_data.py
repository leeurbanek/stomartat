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
    if DEBUG:
        logger.debug(f"start_cli(ctx={type(ctx)}, arguments={arguments})")
    ctx['interface']['command'] = 'data'
    ctx['interface']['data_line'] = ctx['data_service']['data_line']
    ctx['interface']['target_data'] = ctx['data_service']['target_data']

    # add arguments to interface ctx and set database name
    if arguments:  # use symbols in arguments list
        ctx['interface']['arguments'] = sorted([i.upper() for i in list(arguments)])
        ctx['interface']['database'] = click.prompt(
            f"* Using database 'custom.db'. Type a new database name to change,\n  press Enter to accept.", default="custom.db"
        )
    else:  # use symbols in data_service data_list
        ctx['interface']['arguments'] = sorted(list(ctx['data_service']['data_list'].split(' ')))
        ctx['interface']['database'] = click.prompt(
            f"* Using database 'default.db'. Type a new database name to change,\n  press Enter to accept", default="default.db"
        )

    data_line = click.prompt(
        f"* Using data line '{ctx['data_service']['data_line']}'. Type a new value to change,\n  press Enter to accept", default=ctx['data_service']['data_line']
    )
    ctx['interface']['data_line'] = sorted([td.upper() for td in data_line.split(' ')])

    target_data = click.prompt(
        f"* Using target data '{ctx['data_service']['target_data']}'. Type a new value to change,\n  type 'None' to skip, press Enter to accept", default=ctx['data_service']['target_data']
    )
    ctx['interface']['target_data'] = sorted([td.upper() for td in target_data.split(' ')])

    # # Add 'data_line' to 'interface' ctx
    # if data_line:  # use custom values
    #     ctx['interface']['data_line'] = sorted(list(data_line.split(' ')))
    # else:  # use default values
    #     ctx['interface']['data_line'] = sorted(list(ctx['data_service']['data_line'].split(' ')))

    # # Add 'target_data' to 'interface' ctx
    # if target_data:  # use custom value

    #     ctx['interface']['target_data'] = sorted(list(target_data.split(' ')))
    # else:  # use default values
    #     ctx['interface']['target_data'] = sorted(list(ctx['data_service']['target_data'].split(' ')))
    #     if DEBUG: logger.debug(f"target_data: {ctx['interface']['target_data']} {type({ctx['interface']['target_data']})}")

    if click.confirm(f"* Saving {ctx['interface']['data_line']}\n  for {ctx['interface']['arguments']}\n  to '{ctx['interface']['database']}, using target {ctx['interface']['target_data']}.\n  Do you want to continue?"):
        # download data
        from pkg.data_srv import client, utils

        if DEBUG: logger.debug(
            f"cli(ctx={ctx})"
        )
        # check 'data' folder exists in users 'work_dir', if not create folder
        utils.verify_data_folder_exists(ctx=ctx)

        # create sqlite database
        utils.sqlite_create_database(ctx=ctx)

        for index, symbol in enumerate(ctx['interface']['arguments']):
            # if DEBUG: logger.debug(f"index: {index}, symbol: {symbol}")
            ctx['interface']['index'] = index
        #     client.fetch_indicator_data(ctx=ctx, symbol=symbol)

        if DEBUG: logger.debug(f"fetch_target_data(ctx={ctx})")
        if ctx['interface']['target_data'] != 'None':
            for symbol in ctx['interface']['target_data']:
                client.fetch_target_data(ctx=ctx, symbol=symbol)
