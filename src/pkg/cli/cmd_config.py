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
    absolute paths for directories, etc.  Quotes are not necessary.
""")

@click.argument('arguments', nargs=-1, default=None, required=False, type=str)

# config chart_srv, default charts to download
@click.option(
    '--chart-list', 'opt_trans', flag_value='chart_list', help=f"""
    When used without arguments the current list of stock charts to
    download is displayed. Used with one or more arguments: if the
    arguments are symbols in the current list those symbols will be
    removed from the chart download list, if the arguments are not
    in the current list then those symbols will be added to the list.
""")
@click.pass_context
def cli(ctx, arguments, opt_trans):
    """Run config command"""
    if ctx.obj['default']['debug']:
        logger.debug(f"cli(ctx={ctx.obj}, opt_trans={opt_trans})")

    # Add 'arguments' and 'opt_trans' to 'cli' ctx
    ctx.obj['cli']['arguments'] = arguments
    ctx.obj['cli']['opt_trans'] = opt_trans

    cur_sym = ctx.obj['chart_service']['symbol'].split(' ')

    if opt_trans == 'chart_list':
        click.echo(f"Current chart download list: {cur_sym}")

        if arguments:
            # Update chart symbol list
            from pkg.config_srv import chart_symbol
            new_value = chart_symbol.cli_update(ctx)

            if click.confirm(f" Replacing\n\t{cur_sym}\n with:\n\t[{new_value}]\n Do you want to continue?"):
                # Write new list to config file
                config_file = ctx.obj['default']['cfg_chart']
                from pkg.config_srv import utils
                utils.write_config_file(config_file, new_value)
                click.echo(" Done!")
