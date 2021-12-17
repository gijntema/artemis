#
# This file is part of ARTEMIS (https://git.wur.nl/artemis.git).
# Copyright (c) 2021 Wageningen Marine Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""
This Module is a tool to add scenarios as defined in init_param.py to exisiting or newly made config files

Module inputs:
-   make_config.py, specifically the ConfigHandler Object
-   indirectly mapping.py and init_param.py are used by the ConfigHandler object for the functionality of his module

Module Usage:
-   Module is not used directly by any other modules in the model
-   outputs from running this module include configuration csv foil ethat can be used in the main model to
    run batches of scenarios

Last Updated:
    17-12-2021

Version Number:
    0.1
"""

import os
from src.config.init.make_config import ConfigHandler

# Definitions needed for functioning (file names and removal flags)
output_file = 'test_config.csv'          # file that the new scenario will be written to
base_file = 'base_config.csv'                   # template file used if the output file does not exist yet
keep_default_when_using_base = False            # Indicate if the default scenario in the template file should be kept

# quick and dirty way to remove the last two folders from working directory path to assign the right working directory
# likely only works on windows OS
old_dir = os.getcwd()
os.chdir(old_dir.removesuffix('\\tools\\config_tools'))

# check if output file already exists, used to add scenarios to existing scenario csv's
if os.path.isfile(output_file):
    # read output file to identify the scenarios that are already in there
    config_handler = ConfigHandler(output_file)

# if the output does not exist yet, use the base file as basis for new file
else:
    # use a template file if the output file does not exist yet
    config_handler = ConfigHandler('base_config.csv')
    # remove default scenario from template (if specified)
    if not keep_default_when_using_base:
        del config_handler.scenarios_config['default']

# prompt ConfigHandler to read the current values in init_param.py
config_handler.read_scenario_init_param()
# write newly added scenario to the output file
config_handler.remake_scenario_file(output_file=output_file)

# EOF