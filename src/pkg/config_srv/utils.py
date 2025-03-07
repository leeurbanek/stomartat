"""src/pkg/utils/cfg_srv\n
write_file()"""
import logging

from configparser import ConfigParser


logger = logging.getLogger(__name__)


def write_file(ctx: dict):
    """Write new value to the appropriate config file"""
    if ctx['default']['debug']:
        logger.debug(f"write_file(ctx={ctx}, {type(ctx)})")

    # Extract some config info from context object
    config_name = ctx['interface']['config_file']
    config_file = ctx['default'][config_name]
    section = ctx['interface']['section']
    option = ctx['interface']['option']
    new_value = ctx['interface']['new_value']

    # Create getlist() converter, used for reading ticker symbols
    config_obj = ConfigParser(
        allow_no_value=True,
        converters={'list': lambda x: [i.strip() for i in x.split(',')]}
        )
    try:
        config_obj.read(config_file)
    except Exception as e:
        print(e)

    try:
        config_obj.set(section, option, str(new_value))
    except Exception as e:
        print(e)

    # import sys
    # config_obj.write(sys.stdout)
    with open(config_file, 'w') as cf:
        config_obj.write(cf)
