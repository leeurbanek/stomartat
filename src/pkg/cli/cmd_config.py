"""src/pkg/cli/cmd_config.py"""
import logging

import click

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
    absolute paths for directories, etc. Quotes are not necessary.
""")
# TODO cleanup options
@click.argument('arguments', nargs=-1, default=None, required=False, type=str)
# chart_srv, change the default list of charts to download
@click.option(
    '--chart-list', 'opt_trans', flag_value='chart_list', help=f"""
    When used without arguments the current list of stock charts to
    download is displayed. Used with one or more arguments: if the
    arguments are symbols in the current list those symbols will be
    removed from the chart download list, if the arguments are not
    in the current list then those symbols will be added to the list.
""")
# data_srv, change the data lookback period of time
# @click.option(
#     '--db-lookback', 'opt_trans', flag_value='db_lookback', help=f"""
#     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
#     eiusmod tempor incididunt ut labore et dolore magna aliqua.
# """)
# app_default, switch the debug option on/off
@click.option(
    '--debug', 'opt_trans', flag_value='debug', help=f"""
    Displays current debug status (True/False). Entering any argument
    toggles the debug status.
""")
# chart_srv, change the default list of heatmaps to download
@click.option(
    '--heatmap-list', 'opt_trans', flag_value='heatmap_list', help=f"""
    When used without arguments the current list of heatmaps to
    download is displayed. Used with one or more arguments: if the
    arguments are items in the current list those items will be
    removed from the heatmap download list, if the arguments are not
    in the current list then those items will be added to the list.
""")
# # chart_srv, set the webdriver to use
# @click.option(
#     '--webdriver', 'opt_trans', flag_value='webdriver', help=f"""
#     With no arguments: display the current webdriver used. Valid options
#     (arguments) are chrome, gecko.
# """)
# app_default, change location of the default working directory
@click.option(
    '--work-dir', 'opt_trans', flag_value='work_dir', help=f"""
    Use without arguments to display the current work directory.
    To change the location of the working directory enter absolute
    path to the new directory. This will be where the downloaded
    charts and historical price data are kept.
""")

# @click.pass_context
@click.pass_obj
def cli(ctx, arguments, opt_trans):
    """Run config command"""
    # Add 'arguments' and 'opt_trans' to 'interface' ctx
    ctx['interface']['arguments'] = arguments
    ctx['interface']['opt_trans'] = opt_trans

    if ctx['default']['debug']: logger.debug(f"cli(ctx={ctx}, {type(ctx)})")

    if opt_trans == 'chart_list':
        cur_sym = ctx['chart_service'][opt_trans].split(', ')

        if not arguments:
            click.echo(f"Current chart download list: {cur_sym}")
        else:
            # Update chart symbol list
            from pkg.config_srv import utils
            new_value = utils.update_list(ctx=ctx)
            if click.confirm(f" Replacing\n\t{cur_sym}\n with:\n\t[{new_value}]\n Do you want to continue?"):
                ctx['interface']['config_file'] = 'cfg_chart'
                ctx['interface']['section'] = 'chart_service'
                ctx['interface']['option'] = opt_trans
                ctx['interface']['new_value'] = new_value
                # Write new symbol list to config file
                utils.write_file(ctx)
                click.echo(" Done!")

    elif opt_trans == 'db_lookback':
        raise NotImplementedError

    elif opt_trans == 'debug':
        debug_status = (f"{ctx['default']['debug']}")

        if not arguments:
            click.echo(f"Debug status: {debug_status}")
        else:
            # Toggle debug state
            from pkg.config_srv import app_default
            new_value = app_default.update_debug(ctx=ctx)

            if click.confirm(f" Changing debug from: {debug_status} to {new_value}\n Do you want to continue?"):
                # Add config info to context object
                ctx['interface']['config_file'] = 'cfg_main'
                ctx['interface']['section'] = 'default'
                ctx['interface']['option'] = opt_trans
                ctx['interface']['new_value'] = new_value

                # Write new debug state to config file
                from pkg.config_srv import utils
                utils.write_file(ctx)
                click.echo(" Done!")

    elif opt_trans == 'heatmap_list':
        cur_list = ctx['chart_service'][opt_trans].split(', ')

        if not arguments:
            click.echo(f"Current heatmap download list: {cur_list}")
        else:
            # Check arguments are valid
            valid_args = ['1D','1W','1M','3M','6M','YTD','1Y','3Y','5Y','10Y']
            if set(arguments).issubset(valid_args):
                # Update heatmap period list
                from pkg.config_srv import utils
                new_value = utils.update_list(ctx=ctx)
                if click.confirm(f" Replacing\n\t{cur_list}\n with:\n\t[{new_value}]\n Do you want to continue?"):
                    ctx['interface']['config_file'] = 'cfg_chart'
                    ctx['interface']['section'] = 'chart_service'
                    ctx['interface']['option'] = opt_trans
                    ctx['interface']['new_value'] = new_value
                    # Write new symbol list to config file
                    utils.write_file(ctx)
                    click.echo(" Done!")
            else:
                click.echo(f"Valid arguments are:\n  {valid_args}")

    # elif opt_trans == 'scraper':
    #     cur_scrape = (f"{ctx['chart_service']['scraper']}")

    #     if not arguments:
    #         click.echo(f"Current web scraper: '{cur_scrape}'")
    #         click.echo("Valid options are: 'requests', 'selenium'.")

    #     # Check for valid arguments
    #     elif arguments[0] in ['requests', 'selenium']:
    #         # Update work web scraper
    #         from pkg.config_srv import chart
    #         new_value = chart.update_scraper(ctx=ctx)

    #         if click.confirm(f" Replacing\n\t{cur_scrape}\n with:\n\t{new_value}\n Do you want to continue?"):
    #             # Add config info to context object
    #             ctx['interface']['config_file'] = 'cfg_chart'
    #             ctx['interface']['section'] = 'chart_service'
    #             print(f"ctx['interface']['section']: {ctx['interface']['section']}")
    #             ctx['interface']['option'] = opt_trans
    #             ctx['interface']['new_value'] = new_value

    #             # Write web scraper to config file
    #             from pkg.config_srv import utils
    #             utils.write_file(ctx)
    #             click.echo(" Done!")
    #     else:  # try again
    #         click.echo(f"'{arguments[0]}' is not a valid web scraper.")

    elif opt_trans == 'webdriver':
        raise NotImplementedError

    elif opt_trans == 'work_dir':
        cur_wdir = (f"{ctx['default']['work_dir']}")

        if not arguments:
            click.echo(f"Current work directory: {cur_wdir}")
        else:
            # Update work directory
            from pkg.config_srv import app_default
            new_value = app_default.update_work_dir(ctx=ctx)

            if click.confirm(f" Replacing\n\t{cur_wdir}\n with:\n\t{new_value}\n Do you want to continue?"):
                # Add config info to context object
                ctx['interface']['config_file'] = 'cfg_main'
                ctx['interface']['section'] = 'default'
                ctx['interface']['option'] = opt_trans
                ctx['interface']['new_value'] = new_value

                # Write new work directory to config file
                from pkg.config_srv import utils
                utils.write_file(ctx)
                click.echo(" Done!")
