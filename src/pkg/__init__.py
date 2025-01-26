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
    config_obj.set('default', 'debug', 'True')
    # Write the structure to the new file
    with open(config_file, 'w') as fh:
        fh.truncate()
        config_obj.write(fh)
# If config file exists, create configparser object
elif os.path.isfile(config_file):
    config_obj.read(config_file)

# Check if 'debug' setting is valid
if config_obj.get('default', 'debug').lower() in ('1', 'true', 't', 'yes', 'y'):
    config_obj.set('default', 'debug', 'True')
    with open(config_file, 'w') as fh:
        fh.truncate()
        config_obj.write(fh)
else:
    config_obj.set('default', 'debug', 'False')
    with open(config_file, 'w') as fh:
        fh.truncate()
        config_obj.write(fh)

config_obj.read(config_file)

# Gather config files from other apps
cfg_list = []
for root, dirs, files in os.walk(pkg_dir):
    for filename in files:
        if filename.startswith("cfg_") and filename.endswith(".ini"):
            cfg_list.append(os.path.join(root, filename))
# and add them to configparser object
for item in cfg_list:
    config_obj.read(item)

# Put config section/option data into a dictionary
config_dict = dict(
    (section, dict(
        (option, config_obj.get(section, option)) 
        for option in config_obj.options(section)
        )
    ) for section in config_obj.sections()
)

# Convert 'debug' string into a boolean value
config_dict['default']['debug'] = config_dict['default']['debug'] in ('True')

# Print/log some debug information
logger = logging.getLogger(f" === Starting stomartat package ===  src/{__name__}/__init__.py")
if config_dict['default']['debug']: logger.debug(f"""
    root_dir: {root_dir}
    src_dir: {src_dir}
    pkg_dir: {pkg_dir}
    logger_conf: {logger_conf}
    config_file: {config_file}
    config_dict: {config_dict}
""")

# Choose user interface
def run_cli():
    """see 'pyproject.toml' - entry point for CLI"""
    from .cli import main_console
    main_console.start_cli()

def run_gui():
    """see 'pyproject.toml' - entry point for GUI"""
    from .gui import main_window
    main_window.start_gui()
