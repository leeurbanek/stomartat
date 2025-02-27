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
# chart_srv, change the chart skin: light/dark
@click.option(
    '--chart-skin', 'opt_trans', flag_value='chart_skin', help=f"""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua.
""")
# data_srv, change the data lookback period of time
@click.option(
    '--db-lookback', 'opt_trans', flag_value='db_lookback', help=f"""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
    enim ad minim veniam, quis nostrud exercitation ullamco laboris
    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
    in reprehenderit in voluptate velit esse cillum dolore eu fugiat
    nulla pariatur.
""")
# app_default, switch the debug option on/off
@click.option(
    '--debug', 'opt_trans', flag_value='debug', help=f"""
    Displays current debug status (True/False). Entering any argument
    will toggle debug state.
""")
# chart_srv, set the web scraper to use
@click.option(
    '--scraper', 'opt_trans', flag_value='scraper', help=f"""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua.
""")
# app_default, change location of the default working directory
@click.option(
    '--work-dir', 'opt_trans', flag_value='work_dir', help=f"""
    Use without arguments to display the current work directory.
    To change the location of the working directory enter absolute
    path to the new directory. This will be where the downloaded
    charts and historical price data are kept.
""")

@click.pass_context
def cli(ctx, arguments, opt_trans):
    """Run config command"""
    # Add 'arguments' and 'opt_trans' to 'interface' ctx
    ctx.obj['interface']['arguments'] = arguments
    ctx.obj['interface']['opt_trans'] = opt_trans

    if ctx.obj['default']['debug']: logger.debug(f"cli(ctx={ctx.obj})")

    if opt_trans == 'chart_list':
        cur_sym = ctx.obj['chart_service']['chart_list'].split(', ')

        if not arguments:
            click.echo(f"Current chart download list: {cur_sym}")
        else:
            # Update chart symbol list
            from pkg.config_srv import chart
            new_value = chart.update_chart_list(ctx)
            if click.confirm(f" Replacing\n\t{cur_sym}\n with:\n\t[{new_value}]\n Do you want to continue?"):
                ctx.obj['interface']['config_file'] = 'cfg_chart'
                ctx.obj['interface']['section'] = 'chart_service'
                ctx.obj['interface']['option'] = opt_trans
                ctx.obj['interface']['new_value'] = new_value
                # Write new symbol list to config file
                from pkg.config_srv import utils
                utils.write_file(ctx)
                click.echo(" Done!")

    elif opt_trans == 'chart_skin':
        cur_skin = ctx.obj['chart_service']['chart_skin']

        if not arguments:
            click.echo(f"Current chart skin: {cur_skin}")
            click.echo("Valid options are: 'dark', 'light'.")
        # Check for valid arguments
        elif arguments[0] in ['dark', 'light']:
            # Update chart_skin light/dark
            from pkg.config_srv import chart
            new_value = chart.update_chart_skin(ctx)
            if click.confirm(f" Change chart skin from: {cur_skin} to {new_value}\n Do you want to continue?"):
                # Add config info to context object
                ctx.obj['interface']['config_file'] = 'cfg_chart'
                ctx.obj['interface']['section'] = 'chart_service'
                ctx.obj['interface']['option'] = opt_trans
                ctx.obj['interface']['new_value'] = new_value
                # Write new chart skin to config file
                from pkg.config_srv import utils
                utils.write_file(ctx)
                click.echo(" Done!")
        else:  # try again
            click.echo(f"'{arguments[0]}' is not a valid web scraper.")

    elif opt_trans == 'db_lookback':
        raise NotImplementedError

    elif opt_trans == 'debug':
        debug_status = (f"{ctx.obj['default']['debug']}")

        if not arguments:
            click.echo(f"Debug status: {debug_status}")
        else:
            # Toggle debug state
            from pkg.config_srv import app_default
            new_value = app_default.update_debug(ctx=ctx)

            if click.confirm(f" Change debug from: {debug_status} to {new_value}\n Do you want to continue?"):
                # Add config info to context object
                ctx.obj['interface']['config_file'] = 'cfg_main'
                ctx.obj['interface']['section'] = 'default'
                ctx.obj['interface']['option'] = opt_trans
                ctx.obj['interface']['new_value'] = new_value

                # Write new debug state to config file
                from pkg.config_srv import utils
                utils.write_file(ctx)
                click.echo(" Done!")

    elif opt_trans == 'scraper':
        cur_scrape = (f"{ctx.obj['chart_service']['scraper']}")

        if not arguments:
            click.echo(f"Current web scraper: '{cur_scrape}'")
            click.echo("Valid options are: 'requests', 'selenium'.")

        # Check for valid arguments
        elif arguments[0] in ['requests', 'selenium']:
            # Update work web scraper
            from pkg.config_srv import chart
            new_value = chart.update_scraper(ctx)

            if click.confirm(f" Replacing\n\t{cur_scrape}\n with:\n\t{new_value}\n Do you want to continue?"):
                # Add config info to context object
                ctx.obj['interface']['config_file'] = 'cfg_chart'
                ctx.obj['interface']['section'] = 'chart_service'
                print(f"ctx.obj['interface']['section']: {ctx.obj['interface']['section']}")
                ctx.obj['interface']['option'] = opt_trans
                ctx.obj['interface']['new_value'] = new_value

                # Write web scraper to config file
                from pkg.config_srv import utils
                utils.write_file(ctx)
                click.echo(" Done!")
        else:  # try again
            click.echo(f"'{arguments[0]}' is not a valid web scraper.")

    elif opt_trans == 'work_dir':
        cur_wdir = (f"{ctx.obj['default']['work_dir']}")

        if not arguments:
            click.echo(f"Current work directory: {cur_wdir}")
        else:
            # Update work directory
            from pkg.config_srv import app_default
            new_value = app_default.update_work_dir(ctx=ctx)

            if click.confirm(f" Replacing\n\t{cur_wdir}\n with:\n\t{new_value}\n Do you want to continue?"):
                # Add config info to context object
                ctx.obj['interface']['config_file'] = 'cfg_main'
                ctx.obj['interface']['section'] = 'default'
                ctx.obj['interface']['option'] = opt_trans
                ctx.obj['interface']['new_value'] = new_value

                # Write new work directory to config file
                from pkg.config_srv import utils
                utils.write_file(ctx)
                click.echo(" Done!")
