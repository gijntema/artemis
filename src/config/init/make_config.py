
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
        """returns a template filled with (old) default values,
        to initialise the attributes needed to construct configuration with"""

        return template
#        return \
#            {
#                'model':
#                    {
#                        'duration': 50,
#                        'nb_iterations': 1,
#                        'reporting': false
#                    },
#                'agents':
#                    {
#                        'nb_agents': 100,
#                        'catchability_coefficient': 0.2,
#                        'choice_method':
#                            {
#                                'name': 'explore_weighted_heatmap',
#                                'explore_attributes':
#                                    {
#                                        'explore_probability': 0.2,
#                                    },
#                                'heatmap_attributes':
#                                    {
#                                        'init_nb_alternative_known': 4
#                                    }
#                           },
#                        'sharing':
#                            {
#                                'sharing':
#                                    {
#                                        'name': 'random_sharing',
#                                        'no_sharing_attributes': 'DICTIONARY_PLACEHOLDER',
#                                        'random_sharing_attributes': 'DICTIONARY_PLACEHOLDER',
#                                        'nb_options_shared': 10
#                                    },
#                                'receiver_choice':
#                                    {
#                                        'name': 'static_group_choice',
#                                        'group_attributes':
#                                            {
#                                                'nb_groups': 1,
#                                                'group_formation': "equal_mutually_exclusive_groups",
#                                                'group_dynamics': False
#                                            },
#                                        'random_choice_attributes': 'DICTIONARY_PLACEHOLDER',
#                                        'nb_receivers': 10
#                                    },
#                                'receiving':
#                                    {
#                                        'name': 'combine_receiver'
#                                    }
#                            },
#                    },
#               'options':
#                    {
#                        'nb_options': 20,
#                        'growth':
#                            {
#                                'growth_type': 'static',
#                                'growth_attributes':
#                                    {
#                                        'growth_factor': 1
#                                    }
#
#                            },
#                        'stock_reset':
#                            {
#                                'name': 'uniform_random_repeat',
#                                'reset_probability': 0.1,
#                                'uniform_attributes':
#                                    {
#                                        'min_stock': 0,
#                                        'max_stock': 200
#                                    },
#                                'normal_attributes':
#                                    {
#                                        'init_stock': 100,
#                                        'sd_init_stock': 25
#                                    }
#                           }
#                    },
#                'competition':
#                    {
#                        'name': 'interference-simple',
#                        'interference_attributes':
#                            {
#                                'interference_factor': 0.8
#                            }
#                    }
#            }

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------- Initialise configurations as defined in csv file ----------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __read_config_csv(self, filename, separator=';'):
        """reads a config file with scenario settings in csv format"""
        data = pd.read_csv(filename, sep=separator)
        data = data[data['scenario_id'].notna()]
        return data

    def __init_scenarios(self, scenario_file, scenarios='ALL'):
        """loads scenarios from a csv config file and loads these into an internal dictionary (self.scenarios_config),
        by defining a list of scenario names (in strings), only a sub-selection of specified scenarios will be loaded"""
        df_scenarios = self.__read_config_csv(scenario_file)
        if scenarios != 'ALL':
            df_scenarios = df_scenarios[df_scenarios.scenario_id.isin(scenarios)]

        param_columns = [x for x in df_scenarios.columns if x != 'scenario_id']
        for index, row in df_scenarios.iterrows():
            self.scenarios_config[row['scenario_id']] = copy.deepcopy(self.template_config)
            for column in param_columns:
                self.__adjust_parameters(config_key=column.split('|'),
                                         new_value=row[column],
                                         scenario_id=row['scenario_id'],
                                         config_data=self.scenarios_config[row['scenario_id']])

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------- Adjusting a single value in a config ------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __adjust_parameters(self, config_key, new_value, scenario_id, config_data=None):
        if not config_data:
            config_data = self.scenarios_config[scenario_id]

        if isinstance(config_data[config_key[0]], dict):
            self.__adjust_parameters(config_key=config_key[1:],
                                     new_value=new_value,
                                     scenario_id=scenario_id,
                                     config_data=config_data[config_key[0]])

        else:
            config_data[config_key[0]] = new_value

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------- Adding and Exporting scenario's outside of model runs -------------------------------
# ----------------------------------------------------------------------------------------------------------------------
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
        scenario_id, parameter_instructions = ParamConverter().read_init_param_scenario()
        self.add_new_scenario_manually(parameter_instructions=parameter_instructions, scenario_id=scenario_id)

    def remake_scenario_file(self, output_file=None, separator=';'):
        """converts the internal data on scenarios to csv scenario files that can be read in model runs"""
        # 1) define output file
        if not output_file:
            output_file = self.scenario_filename

        if output_file == 'base_config.csv':
            output_file = '{}.'.join(output_file.split(".")).format('_with_adjusted_scenarios')

        # 2) read file structure from old file
        file_structure = pd.read_csv('base_config.csv', sep=separator).columns                                          # TODO: Inflexible quick fix, hardcoded config file structure
        paths = [column for column in file_structure if column != 'scenario_id']

        # 3) convert internal file to pd.Dataframe by reading every scenario and building an intermediate dictionary
        dictionary_for_df = defaultdict(list)
        for scenario in self.scenarios_config:
            dictionary_for_df['scenario_id'].append(scenario)
            for path in paths:
                dictionary_for_df[path].append(self.get_config_value(config_key=path,
                                                                       scenario_id=scenario))

        # 4) export pd Dataframe to output csv
        intermediate_config_df = pd.DataFrame(dictionary_for_df)
        intermediate_config_df.to_csv(output_file, sep=separator, index=False)

    def get_config_value(self, config_key, scenario_id, config_data=None):
        if not config_data:
            config_data = self.scenarios_config[scenario_id]

        if isinstance(config_key, str):
            config_key = config_key.split('|')

        if isinstance(config_data[config_key[0]], dict):
            parameter_value = self.get_config_value(config_key=config_key[1:],
                                    scenario_id=scenario_id,
                                    config_data=config_data[config_key[0]])

        else:
            parameter_value = config_data[config_key[0]]
            return parameter_value

        return parameter_value

#EOF