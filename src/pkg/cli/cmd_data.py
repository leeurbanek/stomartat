"""src/pkg/cli/cmd_data.py"""
import logging

import click


logger = logging.getLogger(__name__)


@click.command('data', short_help="Fetch online OHLC price and volume data")

@click.pass_context
def cli(ctx):
    """Run data command"""
    if ctx.obj['default']['debug']:
        logger.debug(f"cli(ctx={ctx.obj})")
