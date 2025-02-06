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
    The chart utility attempts to fetch online stock charts from
    StockCharts.com.  Charts are saved to the directory specified in
    the config settings.  If no ticker symbols are provided the default
    symbols from the config settings are used.
    Try 'markdata-cli config --help' for help with config settings.
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

@click.pass_context
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
        ctx.obj['interface']['opt_trans'] = period_dict[opt_trans]
    else:  # set default value to daily
        ctx.obj['interface']['opt_trans'] = period_dict['daily']

    # Add 'arguments' to 'interface' ctx
    if arguments:  # download arguments list
        ctx.obj['interface']['arguments'] = [a.upper() for a in list(arguments)]
    else:  # use chart_service chart_list
        ctx.obj['interface']['arguments'] = list(ctx.obj['chart_service']['chart_list'].split(' '))

    if ctx.obj['default']['debug']: logger.debug(f"cli(ctx={ctx.obj})")

    # click.echo(f"Downloading: {ctx.obj['interface']['arguments']}")
    if click.confirm(f"Downloading: {ctx.obj['interface']['arguments']}, {ctx.obj['interface']['opt_trans']}\n Do you want to continue?"):
        # Download charts
        from pkg.chart_srv import client
        client.get_chart(ctx)
    else:  # print default message
        click.echo("Usage: stomartat-cli chart [OPTIONS] [ARGUMENTS]...")

# subprocess.run(['open', filename], check=True)
