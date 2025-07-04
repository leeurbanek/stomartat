"""src/pkg/cli/cmd_config.py"""
import logging

import click

from pkg import DEBUG
from pkg.config_srv import utils


logger = logging.getLogger(__name__)


@click.command('config', short_help="Edit configuration settings", help=
"""
\b
NAME
    config - Edit configuration settings
\b
DESCRIPTION
    The config utility writes specified arguments, separated by a
    single blank space, to the applicable configuration file. Use
    absolute paths for directories. Quotes are not necessary.
""")
@click.argument('arguments', nargs=-1, default=None, required=False, type=str)
# chart_srv, change the default list of charts to download
@click.option(
    '--chart-list', 'opt_trans', flag_value='chart_list', help=f"""
    When used without arguments the current list of stock charts
    to download is displayed. Used with one or more
    arguments: if the arguments are symbols in the current
    list those symbols will be removed from the chart
    download list, if the arguments are not in the current
    list then those symbols will be added to the list.
""")
# chart_srv, set the webdriver to use
@click.option(
    '--chart-webdriver', 'opt_trans', flag_value='chart_webdriver', help=f"""
    With no arguments: display the current webdriver used.
    Valid options (arguments) are chromedriver, geckodriver.
""")
# data_srv, change the data frequency period of time (daily, weekly)
@click.option(
    '--data-frequency', 'opt_trans', flag_value='data_frequency', help=f"""
    With no arguments: display the current sampling period.
    Valid options (arguments) are 'daily', 'weekly',
    'monthly', 'annually'.
""")
# data_srv, change the default list of data lines to download (dataframe columns)
@click.option(
    '--data-line', 'opt_trans', flag_value='data_line', help=f"""
    When used without arguments the current list of data
    lines to download is displayed. Used with one or more
    arguments: if the arguments are in the current list
    those arguments will be removed from the data line list,
    if the arguments are not in the current list then those
    lines will be added to the list. Valid arguments are:
    'clop', 'clv', 'hilo', 'price', 'volume'.
""")
# data_srv, change the default list of ohlc data to download (ticker symbols)
@click.option(
    '--data-list', 'opt_trans', flag_value='data_list', help=f"""
    When used without arguments the current list of stock
    data to download is displayed. Used with one or more
    arguments: if the arguments are symbols in the current
    list those symbols will be removed from the data download
    list, if the arguments are not in the current list then
    those symbols will be added to the list.
""")
# data_srv, change the data lookback period of time (start date)
@click.option(
    '--data-lookback', 'opt_trans', flag_value='data_lookback', help=f"""
    With no argument: display the current lookback period in
    days. Add an integer argument to change the number of
    days in the lookback period.
""")
# data_srv, change the data provider (alphavantage, tiingo, yahoo)
@click.option(
    '--data-provider', 'opt_trans', flag_value='data_provider', help=f"""
    Use without arguments to display the current data
    provider. Valid options are 'alphavantage', 'tiingo' 'yfinance'.
""")
# app_default, switch the debug option on/off
@click.option(
    '--debug', 'opt_trans', flag_value='debug', help=f"""
    Displays current debug status (True/False). Entering any
    argument toggles the debug status.
""")
# chart_srv, change the default list of heatmaps to download
@click.option(
    '--heatmap-list', 'opt_trans', flag_value='heatmap_list', help=f"""
    When used without arguments the current list of heatmaps
    to download is displayed. Used with one or more
    arguments: if the arguments are items in the current list
    those items will be removed from the heatmap download
    list, if the arguments are not in the current list then
    those items will be added to the list.
""")
# TODO need option for sklearn-scaler
# app_default, change location of the default working directory
@click.option(
    '--work-dir', 'opt_trans', flag_value='work_dir', help=f"""
    Use without arguments to display the current work
    directory. To change the location of the working
    directory enter absolute path to the new directory. This
    will be where the downloaded charts and historical price
    data are kept.
""")

# @click.pass_context
@click.pass_obj
def cli(ctx, arguments, opt_trans):
    """Run config command"""
    if DEBUG: logger.debug(f"cli(ctx={ctx}, arguments={arguments}, opt_trans={opt_trans})")

    # Add 'arguments' and 'opt_trans' to 'interface' ctx
    ctx['interface']['arguments'] = arguments
    ctx['interface']['opt_trans'] = opt_trans

    if opt_trans == 'chart_list':
        ctx['interface']['service'] = 'chart_service'

        cur_val = ctx['chart_service'][opt_trans].split(', ')

        if not arguments:
            click.echo(f" Current chart download list: {cur_val}")
        else:
            # Update chart symbol list
            new_value = utils.update_list(ctx=ctx)
            if click.confirm(f" Replacing\n\t{cur_val}\n with:\n\t[{new_value}]\n Do you want to continue?"):
                ctx['interface']['config_file'] = 'cfg_chart'
                ctx['interface']['section'] = 'chart_service'
                ctx['interface']['new_value'] = new_value
                # Write new symbol list to config file
                utils.write_file(ctx)
                click.echo(" Done!")

    elif opt_trans == 'chart_webdriver':
        cur_val = ctx['chart_service']['webdriver']
        valid_arg = ['chromedriver', 'geckodriver']
        new_value = None

        if not arguments:
            click.echo(f" Current webdriver: {cur_val}\n Valid arguments are:\n{valid_arg}")
        else:
            new_value = utils.get_arg_value(ctx=ctx)

        # Check for valid arguments
        if new_value in valid_arg:
            # Update webdriver
            if click.confirm(f" Replacing {cur_val} with {new_value}\n Do you wand to continue?"):
                # Add config info to context object
                ctx['interface']['config_file'] = 'cfg_chart'
                ctx['interface']['section'] = 'chart_service'
                ctx['interface']['new_value'] = new_value

                # Write new webdriver to config file
                utils.write_file(ctx=ctx)
                click.echo(" Done!")
        else:
            click.echo(f" Valid arguments are:\n {valid_arg}")

    elif opt_trans == 'data_line':
        ctx['interface']['service'] = 'data_service'

        cur_val = ctx['data_service'][opt_trans].split(', ')

        if not arguments:
            click.echo(f" Current data line list: {cur_val}")
        else:
            # Update data line list
            new_value = utils.update_list(ctx=ctx)
            if click.confirm(f" Replacing\n\t{cur_val}\n with:\n\t[{new_value}]\n Do you want to continue?"):
                ctx['interface']['config_file'] = 'cfg_data'
                ctx['interface']['section'] = 'data_service'
                ctx['interface']['new_value'] = new_value
                # Write new argument list to config file
                utils.write_file(ctx)
                click.echo(" Done!")

    elif opt_trans == 'data_list':
        ctx['interface']['service'] = 'data_service'

        cur_val = ctx['data_service'][opt_trans].split(', ')

        if not arguments:
            click.echo(f" Current data download list: {cur_val}")
        else:
            # Update data symbol list
            new_value = utils.update_list(ctx=ctx)
            if click.confirm(f" Replacing\n\t{cur_val}\n with:\n\t[{new_value}]\n Do you want to continue?"):
                ctx['interface']['config_file'] = 'cfg_data'
                ctx['interface']['section'] = 'data_service'
                ctx['interface']['new_value'] = new_value
                # Write new symbol list to config file
                utils.write_file(ctx)
                click.echo(" Done!")

    elif opt_trans == 'data_lookback':
        cur_val = ctx['data_service']['data_lookback']

        if not arguments:
            click.echo(f" Current lookback period {cur_val} days")
        else:
            # Update lookback period
            new_value = utils.get_arg_value(ctx=ctx)
            if click.confirm(f" Replacing lookback {cur_val} with {new_value} days.\n Do you want to continue?"):
                ctx['interface']['config_file'] = 'cfg_data'
                ctx['interface']['section'] = 'data_service'
                ctx['interface']['new_value'] = new_value
                # Write new_value to config file
                utils.write_file(ctx=ctx)
                click.echo(" Done!")

    elif opt_trans == 'data_frequency':
        cur_val = ctx['data_service']['data_frequency']
        valid_arg = ['daily', 'weekly', 'monthly', 'annually']

        if not arguments:
            click.echo(f" Data sampling period: {cur_val}\n Valid arguments are: {valid_arg}")
        else:
            # Check arguments are valid
            if set(arguments).issubset(valid_arg):
                # Update sampling period
                new_value = utils.get_arg_value(ctx=ctx)
                if click.confirm(f" Replacing {cur_val} with {new_value}.\n Do you want to continue?"):
                    ctx['interface']['config_file'] = 'cfg_data'
                    ctx['interface']['section'] = 'data_service'
                    ctx['interface']['new_value'] = new_value
                    # Write new symbol list to config file
                    utils.write_file(ctx)
                    click.echo(" Done!")
            else:
                click.echo(f" Valid arguments are:\n {valid_arg}")

    elif opt_trans == 'data_provider':
        cur_val = ctx['data_service']['data_provider']
        valid_arg = ['alphavantage', 'tiingo', 'yfinance']
        new_value = None

        if not arguments:
            click.echo(f" Current data provider: {cur_val}\n Valid arguments are: {valid_arg}")
        else:
            new_value = utils.get_arg_value(ctx=ctx)
            # Check for valid arguments
            # if new_value in valid_arg:
                # Update data provider
                # if click.confirm(f" Replacing {cur_val} with {new_value}.\n Do you wand to continue?"):
                #     # Add config info to context object
    #                 ctx['interface']['config_file'] = 'cfg_data'
    #                 ctx['interface']['section'] = 'data_service'
    #                 ctx['interface']['new_value'] = new_value

    #                 # Write new webdriver to config file
    #                 utils.write_file(ctx=ctx)
    #                 click.echo(" Done!")
    #         else:
    #             click.echo(f" Valid arguments are:\n {valid_arg}")

    elif opt_trans == 'debug':
        cur_val = ctx['default']['debug']

        if not arguments:
            click.echo(f" Debug status: {cur_val}")
        else:
            # Toggle debug state
            new_value = utils.update_debug(ctx=ctx)

            if click.confirm(f" Changing debug from: {cur_val} to {new_value}\n Do you want to continue?"):
                # Add config info to context object
                ctx['interface']['config_file'] = 'cfg_main'
                ctx['interface']['section'] = 'default'
                ctx['interface']['new_value'] = new_value

                # Write new debug state to config file
                utils.write_file(ctx)
                click.echo(" Done!")

    elif opt_trans == 'heatmap_list':
        cur_val = ctx['chart_service'][opt_trans].split(', ')
        valid_arg = ['1D','1W','1M','3M','6M','YTD','1Y','3Y','5Y','10Y']

        if not arguments:
            click.echo(f" Current heatmap download list: {cur_val}\n Valid arguments are:\n{valid_arg}")
        else:
            # Check arguments are valid
            if set(arguments).issubset(valid_arg):
                # Update heatmap period list
                new_value = utils.update_list(ctx=ctx)
                if click.confirm(f" Replacing\n\t{cur_val}\n with:\n\t[{new_value}]\n Do you want to continue?"):
                    ctx['interface']['config_file'] = 'cfg_chart'
                    ctx['interface']['section'] = 'chart_service'
                    ctx['interface']['new_value'] = new_value

                    # Write new symbol list to config file
                    utils.write_file(ctx)
                    click.echo(" Done!")
            else:
                click.echo(f" Valid arguments are:\n {valid_arg}")

    elif opt_trans == 'work_dir':
        cur_val = ctx['default']['work_dir']

        if not arguments:
            click.echo(f" Current work directory: {cur_val}")
        else:
            # Update work directory
            new_value = utils.get_arg_value(ctx=ctx)

            if click.confirm(f" Replacing\n\t{cur_val}\n with:\n\t{new_value}\n Do you want to continue?"):
                # Add config info to context object
                ctx['interface']['config_file'] = 'cfg_main'
                ctx['interface']['section'] = 'default'
                ctx['interface']['new_value'] = new_value

                # Write new work directory to config file
                utils.write_file(ctx)
                click.echo(" Done!")
