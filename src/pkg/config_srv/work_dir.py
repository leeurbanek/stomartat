"""src/pkg/config_srv/work_dir.py
update(ctx)"""
import logging


logger = logging.getLogger(__name__)


def update(ctx):
    """"""
    if ctx.obj['default']['debug']:
        logger.debug(f"update(ctx={ctx.obj}")

    # Get first item in arguments tuple
    new_value = ctx.obj['interface']['arguments'][0]
    return new_value
