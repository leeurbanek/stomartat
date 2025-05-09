"""src/pkg/__init__.py"""
import logging, logging.config
import os

from configparser import ConfigParser


root_dir = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
)))
src_dir = os.path.join(root_dir, 'src/')
work_dir = os.path.join(root_dir, 'temp/')
pkg_dir = os.path.join(root_dir, 'src/pkg')
config_file = os.path.join(src_dir, 'config.ini')
logger_conf = os.path.join(src_dir, 'logger.ini')

logging.config.fileConfig(fname=logger_conf)
logging.getLogger('unittest').setLevel(logging.WARNING)

# Create getlist() converter, used for reading ticker symbols
config_obj = ConfigParser(
    allow_no_value=True,
    converters={'list': lambda x: [i.strip() for i in x.split(',')]}
    )

# Create default config file if if does not exist
if not os.path.isfile(config_file):
    # Add the structure to the configparser object
    config_obj.add_section('default')
    config_obj.set('default', 'debug', 'False')
    config_obj.set('default', 'work_dir', work_dir)
    config_obj.add_section('interface')
    # Write the structure to the new file
    with open(config_file, 'w') as cf:
        cf.truncate()
        config_obj.write(cf)

# Config file exists, create configparser object
try:
    config_obj.read(config_file)
except Exception as e:
    print(f"{e} - {config_file}")

config_obj.read(config_file)

# Gather config files from other apps
for root, dirs, files in os.walk(pkg_dir):
    for filename in files:
        if filename.startswith("cfg_") and filename.endswith(".ini"):
            # put name and path in 'default' section, to be read into confg_dict later
            config_obj.set('default', filename.removesuffix('.ini'), os.path.join(root, filename))
            # read '.ini' paths into configparser object
            config_obj.read(os.path.join(root, filename))

# Put config section/option data into a dictionary
config_dict = dict(
    (section, dict(
        (option, config_obj.get(section, option))
        for option in config_obj.options(section)
        )
    ) for section in config_obj.sections()
)

# Convert 'debug' string into a boolean value
config_dict['default']['debug'] = config_obj.getboolean('default', 'debug')

# Add main config path to config_dict
config_dict['default']['cfg_main'] = config_file

# Print/log some debug information
logger = logging.getLogger(f"  === Starting stomartat package - src/{__name__}/__init__.py ===")
DEBUG = config_dict['default']['debug']
# if config_dict['default']['debug']: logger.debug(f"""
if DEBUG: logger.debug(f"""
    root_dir: {root_dir}
    src_dir: {src_dir}
    work_dir: {work_dir}
    pkg_dir: {pkg_dir}
    logger_conf: {logger_conf}
    config_file: {config_file}
    config_dict: {config_dict}
""")

# # remove old 'debug.log'
# if os.path.exists('debug.log'):
#     os.remove('debug.log')

# Choose user interface
def run_cli():
    """see 'pyproject.toml' - entry point for CLI"""
    from .cli import main_console
    main_console.start_cli()

def run_gui():
    """see 'pyproject.toml' - entry point for GUI"""
    from .gui import main_window
    main_window.start_gui()
