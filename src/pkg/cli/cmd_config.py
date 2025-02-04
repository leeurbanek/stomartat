"""src/pkg/cli/cmd_config.py"""
import logging

import click

logger = logging.getLogger(__name__)


@click.command('config', short_help="Edit configuration settings", help=
"""
\b
NAME
    config - Revise certain configuration settings
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
# TODO add data lookback to cmd_config
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
# app, switch the debug option on/off
@click.option(
    '--debug', 'opt_trans', flag_value='debug', help=f"""
    Displays current debug status (True/False). Entering any argument
    will toggle debug state.
""")
# app, change location of the default working directory
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

    if ctx.obj['default']['debug']:
        logger.debug(f"cli(ctx={ctx.obj})")

    elif opt_trans == 'chart_list':
        cur_sym = ctx.obj['chart_service']['chart_list'].split(', ')

        if not arguments:
            click.echo(f"Current chart download list: {cur_sym}")
        elif arguments:
            # Update chart symbol list
            from pkg.config_srv import chart_symbol
            new_value = chart_symbol.update(ctx)

            if click.confirm(f" Replacing\n\t{cur_sym}\n with:\n\t[{new_value}]\n Do you want to continue?"):
                # Write new symbol list to config file
                from pkg.utils import cfg_srv

                ctx.obj['interface']['config_file'] = 'cfg_chart'
                ctx.obj['interface']['section'] = 'chart_service'
                ctx.obj['interface']['option'] = opt_trans
                ctx.obj['interface']['new_value'] = new_value

                cfg_srv.write_file(ctx)
                click.echo(" Done!")

    if opt_trans == 'debug':
        d_status = (f"{ctx.obj['default']['debug']}")

        if not arguments:
            click.echo(f"Debug status: {d_status}")
        elif arguments:
            # Toggle debug state
            from pkg.config_srv import debug
            new_value = debug.update(ctx)

            if click.confirm(f" Change debug from: {d_status} to {new_value}\n Do you want to continue?"):
                # Write new debug state to config file
                from pkg.utils import cfg_srv

                # Add config info to context object
                ctx.obj['interface']['config_file'] = 'cfg_main'
                ctx.obj['interface']['section'] = 'default'
                ctx.obj['interface']['option'] = opt_trans
                ctx.obj['interface']['new_value'] = new_value

                cfg_srv.write_file(ctx)
                click.echo(" Done!")

    elif opt_trans == 'work_dir':
        cur_wdir = (f"{ctx.obj['default']['work_dir']}")

        if not arguments:
            click.echo(f"Current work directory: {cur_wdir}")
        elif arguments:
            # Update work directory
            from pkg.config_srv import work_dir
            new_value = work_dir.update(ctx)

            if click.confirm(f" Replacing\n\t{cur_wdir}\n with:\n\t{new_value}\n Do you want to continue?"):
                # Write new work directory to config file
                from pkg.utils import cfg_srv

                # Add config info to context object
                ctx.obj['interface']['config_file'] = 'cfg_main'
                ctx.obj['interface']['section'] = 'default'
                ctx.obj['interface']['option'] = opt_trans
                ctx.obj['interface']['new_value'] = new_value

                cfg_srv.write_file(ctx)
                click.echo(" Done!")
