"""src/pkg/config_srv/app_default.py\n
update_debug(ctx)\n
update_work_dir(ctx)"""
import logging


logger = logging.getLogger(__name__)


def update_debug(ctx: dict):
    """Enter any character to toggle debug (logging) status."""
    if ctx['default']['debug']:
        logger.debug(f"update_debug(ctx={ctx}, {type(ctx)}")

    # Get first item in arguments tuple
    new_value = not ctx['default']['debug']
    return new_value


def update_work_dir(ctx: dict):
    """Enter an absolute path to change the work directory location."""
    if ctx['default']['debug']:
        logger.debug(f"update_work_dir(ctx={ctx}, {type(ctx)}")

    # Get first item in arguments tuple
    new_value = ctx['interface']['arguments'][0]
    return new_value
