"""src/pkg/config_srv/default.py
update_debug(ctx)
update_work_dir(ctx)"""
import logging


logger = logging.getLogger(__name__)


def update_debug(ctx):
    """"""
    if ctx.obj['default']['debug']:
        logger.debug(f"update(ctx={ctx.obj}")

    # Get first item in arguments tuple
    new_value = not ctx.obj['default']['debug']
    return new_value


def update_work_dir(ctx):
    """"""
    if ctx.obj['default']['debug']:
        logger.debug(f"update(ctx={ctx.obj}")

    # Get first item in arguments tuple
    new_value = ctx.obj['interface']['arguments'][0]
    return new_value
