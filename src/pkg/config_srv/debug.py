"""src/pkg/config_srv/debug.py
update(ctx)"""
import logging


logger = logging.getLogger(__name__)


def update(ctx):
    """"""
    if ctx.obj['default']['debug']:
        logger.debug(f"update(ctx={ctx.obj}")

    # Get first item in arguments tuple
    new_value = not ctx.obj['default']['debug']
    return new_value
