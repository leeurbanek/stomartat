"""src/pkg/cli/cmd_heatmap.py"""
import logging

import click

from pkg import DEBUG


logger = logging.getLogger(__name__)


@click.command('heatmap', short_help="Fetch online S&P heatmaps", help=
"""
\b
NAME
    heatmap - Fetch online S&P heatmaps
\b
DESCRIPTION
    The heatmap utility fetches S&P 500 heatmaps from stockanalysis.com.
    Downloaded heatmaps are saved to the work directory specified in
    the config settings. If no heatmap times (arguments) are provided
    the default list is used. Possible time arguments are: 1D, 1W, 1M,
    3M, 6M, YTD, 1Y, 3Y, 5Y, 10Y.
""")

@click.argument(
    'arguments', nargs=-1, default=None, required=False, type=str
)

# @click.pass_context
@click.pass_obj
def cli(ctx, arguments):
    """Run heatmap command"""
    if DEBUG: logger.debug(f"start_cli(ctx={type(ctx)}, arguments={arguments})")
    ctx['interface']['command'] = 'heatmap'

    # Add 'arguments' to 'interface' ctx
    if arguments:  # download heatmaps in arguments list
        ctx['interface']['arguments'] = sorted([a.upper() for a in list(arguments)])
    else:  # use chart_service heat_map list
        ctx['interface']['arguments'] = sorted(list(ctx['chart_service']['heatmap_list'].split(' ')))

    if DEBUG: logger.debug(f'cli(ctx={ctx})')

    if click.confirm(f" Downloading: {ctx['interface']['arguments']}\n Do you want to continue?"):
        # Download heatmaps
        from pkg.chart_srv import client
        client.begin_chart_download(ctx)
    else:  # Print default message
        click.echo("Goodby.")
