"""src/pkg/cli/cmd_chart.py"""
import logging

import click


logger = logging.getLogger(__name__)


@click.command('chart', short_help="Fetch online stockcharts", help=
"""
\b
NAME
    chart - Fetch online stockcharts
\b
DESCRIPTION
    The chart utility fetches candle stick charts from StockCharts.com.
    Downloaded charts are saved to the work directory specified in
    the config settings. If no ticker symbols (arguments) are provided
    the default symbol list is used. If no options (period) is given
    daily charts are downloaded.
""")

@click.argument(
    'arguments', nargs=-1, default=None, required=False, type=str
)
@click.option(
    '-a', '--all', 'opt_trans', flag_value='all', help='Fetch daily and weekly charts.'
)
@click.option(
    '-d', '--daily', 'opt_trans', flag_value='daily', help='Fetch only daily charts.'
)
@click.option(
    '-w', '--weekly', 'opt_trans', flag_value='weekly', help='Fetch only weekly charts.'
)

# @click.pass_context
@click.pass_obj
def cli(ctx, arguments, opt_trans):
    """Run chart command"""

    # Put option flag_value into dictionary of lists
    period_dict = {
        'all': ['Daily', 'Weekly'],
        'daily': ['Daily', ],
        'weekly': ['Weekly', ]
        }

    # Add 'opt_trans' to 'interface' ctx
    if opt_trans:  # use period_dict value
        ctx['interface']['opt_trans'] = period_dict[opt_trans]
    else:  # set default value to daily
        ctx['interface']['opt_trans'] = period_dict['daily']

    # Add 'arguments' to 'interface' ctx
    if arguments:  # download charts in arguments list
        ctx['interface']['arguments'] = sorted([a.upper() for a in list(arguments)])
    else:  # use chart_service chart_list
        ctx['interface']['arguments'] = sorted(list(ctx['chart_service']['chart_list'].split(' ')))

    if ctx['default']['debug']: logger.debug(f'cli(ctx={ctx} {type(ctx)})')

    if click.confirm(f"Downloading: {ctx['interface']['arguments']}, {ctx['interface']['opt_trans']}\n Do you want to continue?"):
        # Download charts
        from pkg.chart_srv import client
        client.get_chart(ctx)
    else:  # Print default message
        click.echo("Goodby.")
