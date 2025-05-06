"""src/pkg/cli/main_console.py"""
import logging
import os

import click

from pkg import config_dict, DEBUG


logger = logging.getLogger(__name__)


class MyMultiCommand(click.MultiCommand):
    """Parse files that start with 'cmd_' located in this directory"""

    def list_commands(self, ctx):
        cmd_list = []
        for filename in os.listdir(os.path.abspath(os.path.dirname(__file__))):
            if filename.startswith("cmd_") and filename.endswith(".py"):
                cmd_list.append(filename[4:-3])
        cmd_list.sort()
        return cmd_list

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"pkg.cli.cmd_{name}", None, None, ["cli"])
        except ImportError:
            return
        return mod.cli


@click.command(cls=MyMultiCommand)

@click.pass_context
def start_cli(ctx):
    """"""
    ctx.obj = config_dict
    if DEBUG: logger.debug(f"start_cli(ctx={ctx.obj}, {type(ctx)})")
