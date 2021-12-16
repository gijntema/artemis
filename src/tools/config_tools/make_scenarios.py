import os
from src.config.init.make_config import ConfigHandler

old_dir = os.getcwd()
os.chdir(old_dir.removesuffix('\\tools\\config_tools'))  # quick and dirty way to removethe last two folders from working directory path, likely only works on windows

output_file = 'scenario_testing_x.csv'          # file that the new scenario will be written to
base_file = 'base_config.csv'                   # base file used to add a scenario to
keep_default_when_using_base = False            # remove 'default' from base file

# check if output file already exists, used to add scenarios to existing scenario csvs
if os.path.isfile(output_file):
    config_handler = ConfigHandler(output_file)

# if the output does not exist yet, use the base file as basis for new file
else:
    config_handler = ConfigHandler('base_config.csv')
    if not keep_default_when_using_base:
        del config_handler.scenarios_config['default']

config_handler.read_scenario_init_param()
config_handler.remake_scenario_file(output_file=output_file)

# EOF