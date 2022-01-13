
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
This Module has two aims:
1)  defining the container for model configurations with regards to parameter setting and scenarios,
    as read from a scenario file.
2)  return the appropriate parameters when asked for in different parts of the model run # TODO: UNIMPLEMENTED in main modules
3)  serve as a, model independent, tool to build new scenarios manually

this module is read by ARTEMIS.py to determine all parameter variables and scenarios.
this module can be accessed separately of the model to add model scenarios to scenario .csv files

Module inputs:
-   Scenario csv files

Module Usage:
-   all defined variables are used to add a scenario to a config .csv

Last Updated:
    24-11-2021

Version Number:
    0.1
"""

import json
import csv
import os
import copy
import pandas as pd
from collections import defaultdict
from src.config.init.param_to_config_mapping import ParamConverter
from src.config.init.config_template import template

class ConfigHandler:
    """class the reads configurations from a file and provides the appropriate
    configurations at different locations in the model"""

    def __init__(self, scenario_file='base_config.csv'):
        self.scenario_filename = scenario_file
        self.template_config = self.__init_template_param()                                                             # make a template configuration that can be adjusted to scenario values
        self.scenarios_config = {}                                                                                      # initialise a dictionary data container to hold configurations for all scenarios to be tested
        self.__init_scenarios(scenario_file)                                                                            # load the scenarios as defined in the scenario file

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------- Initialise a template for model configurations -----------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __init_template_param(self):
        """returns a template filled with (old) default values (as defined in config_template.py,
        to initialise the attributes needed to construct configuration with"""

        return template

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------- Read scenario configurations as defined in csv file ---------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def __init_scenarios(self, scenario_file, scenarios='ALL'):
        """loads scenarios from a csv config file and loads these into an internal dictionary (self.scenarios_config),
        by defining a list of scenario names (in strings), only a sub-selection of specified scenarios will be loaded"""

        df_scenarios = self.__read_config_csv(scenario_file)                                                            # read scenario csv file
        if scenarios != 'ALL':                                                                                          # if specified that the model should not read all scenarios but only a specified subset
            df_scenarios = df_scenarios[df_scenarios.scenario_id.isin(scenarios)]                                       # only include the scenarios that were specified

        param_columns = [x for x in df_scenarios.columns if x != 'scenario_id']                                         # make a list of columns that need to be read to get parameter settings
        for index, row in df_scenarios.iterrows():                                                                      # iterate over rows (indvidual scenarios)
            self.scenarios_config[row['scenario_id']] = copy.deepcopy(self.template_config)                             # make an template entry (to be changed) for the scenario (scenario name as key) in the internal dictionary of the ConfigHandler object

            for column in param_columns:                                                                                # loop over all parameters settings of an indiviudal scenario
                self.__adjust_parameters(config_key=column.split('|'),                                                  # split the column name to get a list of dictionary keys
                                         new_value=row[column],                                                         # access the parameter value for the considered scenario
                                         scenario_id=row['scenario_id'],                                                # access the scenario name of the considered scenario
                                         config_data=self.scenarios_config[row['scenario_id']])                         # change the considered parameter form the template value to the setting of the currently considered scenario

    def __read_config_csv(self, filename, separator=';'):
        """reads a config file with scenario settings in csv format, default separator
        (if separator is not defined) is assumed to be ;"""

        data = pd.read_csv(filename, sep=separator)                                                                     # read csv scenario file
        data = data[data['scenario_id'].notna()]                                                                        # remove scenarios that have no scenario name

        return data                                                                                                     # csv data return statement

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------- Adjusting a single value in a config ------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __adjust_parameters(self, config_key, new_value, scenario_id, config_data=None):
        """"changes one specific value, based on a nest dictionary key given as a list,
         in a ConfigHandler internal dictionary format that holds the information on all scenario parameter settings,
         for a specified scenario in a given dictionary"""

        if not config_data:                                                                                             # if the iternal dictionary to be changed is not specified, start at the top of the specified scenario entry in the ConfigHandler internal settings dictionary
            config_data = self.scenarios_config[scenario_id]

        if isinstance(config_data[config_key[0]], dict):                                                                # handle nested levels in the dictionaries: access the data present using the first part of the key, if this does not lead to a value to change, take the second part of the key to look further etc.
            self.__adjust_parameters(config_key=config_key[1:],                                                         # cut off the first part of the dictionary key
                                     new_value=new_value,                                                               # repeat what value we are changing
                                     scenario_id=scenario_id,                                                           # repeat what scenario we are changing
                                     config_data=config_data[config_key[0]])                                            # define the nested dictionary found as the new dictionary to change a value in

        else:                                                                                                           # if the part of the dictionary that is accessed by the key is a value that can be changed:
            config_data[config_key[0]] = new_value                                                                      # change the value

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------- Adding and Exporting scenario's outside of model runs -------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    # TODO: MOVE BELOW FUNCTIONALITY TO (CHILD) CLASS IN OTHER MODULE TO KEEP MODEL FUNCTIONALITY AND TOOLS SEPARATE

    def add_new_scenario_manually(self, parameter_instructions, scenario_id):
        """adds a scenario to the internal configuration scenario dictionary.
        adjusts the default values from the internal template (self.template_config) according to parameter instructions
        Parameter instructions to create a new scenario need to be formatted as a list of tuples with (path, value):
        e.g. [('agents|catchability_coefficient', 0.5), ('agents|sharing|receiver_choice|nb_receivers', 1)]"""

        self.scenarios_config[scenario_id] = copy.deepcopy(self.template_config)                                        # ensure the new scenario has an entry with the config template in it
        for path, value in parameter_instructions:                                                                      # unpack every parameter change instruction in a for loop
            self.__adjust_parameters(config_key=path.split('|'), new_value=value, scenario_id=scenario_id)              # adjust the parameters in the template

    def read_scenario_init_param(self):
        """uses values defined in init_param.py to add a new configuration scenario,
        based on the mapping provided by the class param_to_config_mapping.ParamConverter"""

        scenario_id, parameter_instructions = ParamConverter().read_init_param_scenario()                               # read init_param values
        self.add_new_scenario_manually(parameter_instructions=parameter_instructions, scenario_id=scenario_id)          # load init_paran values as scenario in ConfigHandler internal dictionary

    def remake_scenario_file(self, output_file=None, separator=';'):
        """converts the internal data on scenarios to csv scenario files that can be read in future model runs"""

        # 1) define output file
        if not output_file:                                                                                             # if an output file is not defined
            output_file = self.scenario_filename                                                                        # use file that was read to construct current internal dictionary of ConfigHandler

        if output_file == 'base_config.csv':                                                                            # ensure that base_config.csv is never overwritten, as it may be used as template file
            output_file = '{}.'.join(output_file.split(".")).format('_with_adjusted_scenarios')                         # add a suffix to ensure base_config is not overwritten

        # 2) read file structure from old file
        file_structure = pd.read_csv('base_config.csv', sep=separator).columns                                          # discern the structure (the columns that shoiul dbe in an output file) an ouput file should have by reading base_config.csv as template
        paths = [column for column in file_structure if column != 'scenario_id']                                        # get the column names that parameter values need to be loaded to

        # 3) convert internal file to pd.Dataframe by reading every scenario and building an intermediate dictionary
        dictionary_for_df = defaultdict(list)                                                                           # make an empty data dictionary to load values to in the structure needed for exporting the scenario file
        for scenario in self.scenarios_config:                                                                          # loop over all scenario settings currently loaded in the ConfigHandler object
            dictionary_for_df['scenario_id'].append(scenario)                                                           # attach scenario id to intermediate dictionary
            for path in paths:                                                                                          # for every column (as dictionary key):
                dictionary_for_df[path].append(self.get_config_value(config_key=path,                                   # attach the value in the intermediate dictionary
                                                                       scenario_id=scenario))

        # 4) export pd Dataframe to output csv
        intermediate_config_df = pd.DataFrame(dictionary_for_df)                                                        # convert intermediate dictionary to pandas dataframe (easier for exporting)
        intermediate_config_df.to_csv(output_file, sep=separator, index=False)                                          # Export pandas dataframe with scenario settings to scenario file

    def get_config_value(self, config_key, scenario_id, config_data=None):
        """looks up and returns the value in the currently loaded scenario settings in the ConfigHandler object"""
        if not config_data:
            config_data = self.scenarios_config[scenario_id]

        if isinstance(config_key, str):
            config_key = config_key.split('|')

        if isinstance(config_key, list):
            if isinstance(config_data[config_key[0]], dict):                                                            # handle nested levels in the dictionaries: access the data present using the first part of the key, if this does not lead to a value to change, take the second part of the key to look further etc.
                parameter_value = self.get_config_value(config_key=config_key[1:],                                      # cut off the first entry of the dictionary key
                                                        scenario_id=scenario_id,                                        # repeat in what scenario a value is being looked up
                                                        config_data=config_data[config_key[0]])                         # use the nested dictionary as new dictionary to look up the value

            else:
                parameter_value = config_data[config_key[0]]                                                            # if the key leads to a value
                return parameter_value                                                                                  # return the value found


        else:
            raise TypeError("Config key to look up values for scenario settings can only be strings, "
                            "value now is a {}".format(type(config_key)))

        return parameter_value                                                                                          # return the value found



#EOF