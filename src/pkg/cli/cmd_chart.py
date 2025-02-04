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


# import logging
# from configparser import ConfigParser

# import click

# from src import config_file
# from src.chart_service import client

# conf_obj = ConfigParser(
#     converters={'list': lambda x: [i.strip() for i in x.split(',')]}
#     )
# conf_obj.read(config_file)

# logger = logging.getLogger(__name__)

# @click.command('chart', short_help="Fetch online stockcharts from StockCharts.com", help="""
# \b
# NAME
#     chart -- Get online stock charts from StockChart.com
# \b
# SYNOPSIS
#     chart [Options] [ticker1 ticker2 ticker3 ...]
# \b
# DESCRIPTION
#     The chart utility attempts to fetch online stock charts from
#     StockCharts.com.  Charts are saved to the directory specified in
#     the config settings.  If no ticker symbols are provided the default
#     symbols from the config settings are used.
#     Try 'markdata-cli config --help' for help with config settings.
# """)

# @click.argument('symbol', nargs=-1, default=None, required=False, type=str)

# @click.option('--all', 'opt_trans', flag_value='all', help='Fetch daily and weekly charts.')
# @click.option('--daily', 'opt_trans', flag_value='daily', help='Fetch only daily charts.')
# @click.option('--weekly', 'opt_trans', flag_value='weekly', help='Fetch only weekly charts.')

# @click.pass_context
# def cli(ctx, opt_trans, symbol):
#     """Run chart command"""
#     if ctx.obj['debug']:
#         logger.debug(f"cli(ctx, opt_trans={opt_trans}, symbol={symbol })")

#     if opt_trans:
#         # option flag_value to dictionary of lists
#         period_dict = {
#             'all': ['Daily', 'Weekly'],
#             'daily': ['Daily', ],
#             'weekly': ['Weekly', ]
#             }
#         period = period_dict[opt_trans]

#         if symbol:  # use symbols from command line input
#             symbol = [s.upper() for s in list(symbol)]
#         else:  # use symbols from config.ini
#             symbol = conf_obj.getlist('Ticker', 'symbol')

#         # add parameters to context object
#         ctx.obj['opt_trans'] = opt_trans
#         ctx.obj['period'] = period
#         ctx.obj['symbol'] = symbol

#         client.get_chart(ctx.obj)

#     else:  # print default message
#         click.echo(f"""Usage: markdata chart [OPTIONS] [SYMBOL]...
# Try 'markdata chart --help' for help.""")

# # subprocess.run(['open', filename], check=True)
