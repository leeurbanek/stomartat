"""src/pkg/config_srv/utils.py\n
write_config_file()"""
import logging
import sys

from configparser import ConfigParser


logger = logging.getLogger(__name__)


def write_config_file(ctx):
    """Write new value to the appropriate config file"""
    if ctx.obj['default']['debug']:
        logger.debug(f"write_config_file(ctx: {ctx.obj})")

    # Extract some config info from context object
    config_name = ctx.obj['interface']['config_file']
    config_file = ctx.obj['default'][config_name]
    section = ctx.obj['interface']['section']
    option = ctx.obj['interface']['option']
    new_value = ctx.obj['interface']['new_value']

    # Create getlist() converter, used for reading ticker symbols
    config_obj = ConfigParser(
        allow_no_value=True,
        converters={'list': lambda x: [i.strip() for i in x.split(',')]}
        )

    try:
        config_obj.read(config_file)
    except Exception as e:
        print(e)

    config_obj.set(section, option, new_value)

    # config_obj.write(sys.stdout)
    with open(config_file, 'w') as cf:
        config_obj.write(cf)
