"""src/pkg/cli/cmd_chart.py"""
import logging

import click


logger = logging.getLogger(__name__)


@click.command('chart', short_help="Fetch online stockcharts from StockCharts.com")

@click.pass_context
def cli(ctx):
    """Run chart command"""
    if ctx.obj['default']['debug']:
        logger.debug(f"cli(ctx={ctx.obj})")
