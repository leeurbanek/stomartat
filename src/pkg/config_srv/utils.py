"""src/pkg/config_srv/utils.py\n
write_config_file()"""
import logging

from pkg import config_obj


logger = logging.getLogger(__name__)


def write_config_file(config_file, new_value):
    """Write new value to config.ini"""
    if config_obj['default']['debug']:
        logger.debug(f"write_config_file(config_file={config_file}, new_value={new_value})")

    config_obj['chart_service']['symbol'] = new_value

    with open(config_file, 'w') as cf:
        config_obj.write(cf)
