"""src/pkg/utils/cfg_srv\n
write_file()"""
import logging

from configparser import ConfigParser


logger = logging.getLogger(__name__)


def write_file(ctx):
    """Write new value to the appropriate config file"""
    if ctx.obj['default']['debug']:
        logger.debug(f"write_file(ctx: {ctx.obj})")

    # Extract some config info from context object
    config_name = ctx.obj['interface']['config_file']
    config_file = ctx.obj['default'][config_name]
    section = ctx.obj['interface']['section']
    print(f"section: {section}")

    option = ctx.obj['interface']['option']
    print(f"option: {option}")

    new_value = ctx.obj['interface']['new_value']
    print(f"new_value: {new_value}")

    # Create getlist() converter, used for reading ticker symbols
    config_obj = ConfigParser(
        allow_no_value=True,
        converters={'list': lambda x: [i.strip() for i in x.split(',')]}
        )

    try:
        print(f"config_file: {config_file}")
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
