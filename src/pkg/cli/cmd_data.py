"""src/pkg/cli/cmd_data.py"""
import logging

import click

from pkg import config_dict, DEBUG


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
@click.option(
    '--line', 'data_line',
    prompt='* Using default data_line list.  Type in specific lines to download,\n  press Enter to accept default lines',
    prompt_required=True,
    default=config_dict['data_service']['data_line'],
    help='Select which data lines to save.'
)
@click.option(
    '--target', 'target_data',
    prompt='* Using default target symbol.  Type in specific target to download,\n  press Enter to accept default target symbol',
    prompt_required=True,
    default=config_dict['data_service']['target_data'],
    help='Select which target symbol to download.'
)

# @click.pass_context
@click.pass_obj
def cli(ctx, arguments, data_line, target_data):
    """Run data command"""
    ctx['interface']['command'] = 'data'

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

    # Add 'data_line' to 'interface' ctx
    if data_line:  # use custom values
        ctx['interface']['data_line'] = sorted(list(data_line.split(' ')))
    else:  # use default values
        ctx['interface']['data_line'] = sorted(list(ctx['data_service']['data_line'].split(' ')))

    # Add 'target_data' to 'interface' ctx
    if target_data:  # use custom value
        ctx['interface']['target_data'] = target_data
    else:  # use default values
        ctx['interface']['target_data'] = ctx['data_service']['target_data']

    if click.confirm(f"* Saving {ctx['interface']['data_line']}\n  for {ctx['interface']['arguments']}\n  to '{ctx['interface']['database']}, using target '{ctx['interface']['target_data']}.'\n  Do you want to continue?"):
        # download data
        from pkg.data_srv import client, utils

        if DEBUG: logger.debug(
            f"cli(ctx={ctx}, arguments={ctx['interface']['arguments']})"
        )
        # check 'data' folder exists in users 'work_dir', if not create folder
        utils.verify_data_folder_exists(ctx=ctx)

        # create sqlite database
        utils.sqlite_create_database(ctx=ctx)

        for index, symbol in enumerate(ctx['interface']['arguments']):
            ctx['interface']['index'] = index
            # client.get_ohlc_data(ctx=ctx, symbol=symbol)
