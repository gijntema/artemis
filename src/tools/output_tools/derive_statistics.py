
# SEE BOTTOM FOR EXECUTION OF SCRIPT -- ALSO DEFINE PROPER SCENARIO FILE THERE

from src.tools.output_tools.export_data import DataWriter
import pandas as pd
import re
import copy
import os
import numpy as np

class StatisticsDeriver:
    """Class to derive statistics and measures
    from two raw output data .csv files of ARTEMIS.py for a single run scenario"""
# ----------------------------------------------------------------------------------------------------------------------
# Initialisation Methods
# ----------------------------------------------------------------------------------------------------------------------

    def __init__(self,
                 scenario_name,
                 output_folder_name='output/data_output/',
                 flat_time_x_agent_file_name_template='flat_time_x_agent_results{}.csv',
                 flat_time_x_environment_file_name_template='flat_time_x_environment_results{}.csv'):

        self.flat_time_x_agent_path_template = output_folder_name + flat_time_x_agent_file_name_template
        self.flat_time_x_environment_path_template = output_folder_name + flat_time_x_environment_file_name_template

        self.functionality = self.__init_functionality()

        self.flat_time_x_agent_data = pd.read_csv(self.flat_time_x_agent_path_template.format(scenario_name))
        self.flat_time_x_environment_data = pd.read_csv(self.flat_time_x_environment_path_template.format(scenario_name))

        self.flat_time_x_environment_data['agents_visited'] = \
            self.flat_time_x_environment_data['agents_visited'].fillna('')                                              # convert nan values to empty strings to prevent bugging in later stages of the data analysis

        self.data_writer = DataWriter(output_file_suffix="with_statistics_{}".format(scenario_name))


    def __init_functionality(self):
        return \
            {
                'flat_time_x_agent':
                    {
                        "mean_absolute_error": self.__derive_statistics_flat_time_x_agent_mean_absolute_error
                        # INSERT FURTHER FUNCTIONALITY HERE
                    },
                'flat_time_x_environment':
                    {
                        "agent_heatmap_errors": self.__derive_statistics_flat_time_x_environment_heatmap_errors
                    }
            }

# ----------------------------------------------------------------------------------------------------------------------
# Main Functionality Methods for Deriving Statistics and Measures
# ----------------------------------------------------------------------------------------------------------------------

    def derive_statistics_flat_time_x_agent(self):
        # 1) loop over scenarios defined in the config file
        # 2) read files (time_x_agent and time_x_environment)
        # 3) loop over time steps
        # 4) loop over agents
        # 5) add data point to data series
        # 6) attach data series as new column
        # 7) export data
        pass

    def derive_statistics_flat_time_x_environment(self):
        self.functionality['flat_time_x_environment']["agent_heatmap_errors"]()

# ----------------------------------------------------------------------------------------------------------------------
# Supporting Methods Called by Main Functionality for Deriving Statistics and Measures Time and Agent Specific
# ----------------------------------------------------------------------------------------------------------------------

    def __derive_statistics_flat_time_x_agent_mean_absolute_error(self):
        pass

# ----------------------------------------------------------------------------------------------------------------------
# Supporting Methods Called by Main Functionality for Deriving Statistics and Measures Time and Environment Specific
# ----------------------------------------------------------------------------------------------------------------------

    def __derive_statistics_flat_time_x_environment_heatmap_errors(self):

        # 0) define pattern to search for in column names using regular expressions
        regex = re.compile(r'(agent_\d*)')

        # 1) # get Column names
        column_names = copy.deepcopy(list(self.flat_time_x_environment_data.columns))

        # 2) list comprehension in combination with regular expression to find agent names
        agents = [re.findall(regex, column) for column in column_names]

        # 3) select only columns that refer to an a value for an individual agent (have 'agent_<##>' in the column name)
        agents = [column for column in agents if len(column) > 0]

        # 4) list comprehension fist instance of list in list is new list entry (re.findall returns a list with values)
        agents = [agent[0] for agent in agents]

        # 5) find only unique agents in columns (the set object can only obtain unique values)
        agents = set(agents)
        agents = list(agents)
        agents.sort()

        # 6) loop over unique agents
        for agent in agents:
            # 7) Make Agent Error column with the real value (potential_catch) - predicted value (heatmap expectation)
            df = self.flat_time_x_environment_data                                                                      # give the data to be modified an additional, shorter, name for easier readability in the script
            df['{}_heatmap_error'.format(agent)] = \
                df.apply(lambda row: self.__lambda_heatmap_errors(row=row, agent=agent), axis=1)                        # Use function __lambda_heatmap_errot to calculate the errors for every row and

        # 8) export data
        self.__export_derivative_statistics_time_x_environment()

    def __lambda_heatmap_errors(self, row, agent):
        """supporting function of derive __derive_statistics_flat_time_x_environment_heatmap_errors
        that assesses the conditionals and does the actual calculations of errors"""
        if agent in row['agents_visited'].split('|'):
            corrected_catch = row['{}_catch_potential'.format(agent)] * row['occurred_competition_correction']

        else:
            corrected_catch = row['{}_catch_potential'.format(agent)] * row['hypothetical_competition_correction']

        error = corrected_catch - row['{}_catch_expectation_heatmap'.format(agent)]
        return error

# ----------------------------------------------------------------------------------------------------------------------
# Supporting Methods Called by Main Functionality for Deriving Statistics and Measures in general
# ----------------------------------------------------------------------------------------------------------------------

    def __export_derivative_statistics_time_x_environment(self):
        self.data_writer.write_csv(self.flat_time_x_environment_data, 'flat_time_x_environment_results_with_statistics_')

    def __export_derivative_statistics_time_x_agent(self):
        self.data_writer.write_csv(self.flat_time_x_environment_data, 'flat_time_x_agent_results_with_statistics_')

# ----------------------------------------------------------------------------------------------------------------------
# EXECUTING THE SCRIPT

# 0) set proper wd
old_dir = os.getcwd()
os.chdir(old_dir.removesuffix('\\tools\\output_tools'))

# 1) read scenario_file and get list of scenarios
scenarios = pd.read_csv('base_config.csv', sep=';')
scenarios = scenarios['scenario_id'].values
scenarios = np.unique(scenarios)

# 2) loop over scenarios
for scenario in scenarios:

    # 3) Initialise StatisticsDeriver for scenario (and read accompanying dat files)
    deriver = StatisticsDeriver(scenario_name=scenario, output_folder_name='output/data_output/')

    # 4) Derive environment statistics
    deriver.derive_statistics_flat_time_x_environment()

    # 5) derive agent statistics
    deriver.derive_statistics_flat_time_x_agent()  # Unsupported

    # 6?) others statistics
    # NA



# EOF
