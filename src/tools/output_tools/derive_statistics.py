

# TODO: UNFINSIHED MODULE


from src.tools.output_tools.export_data import DataWriter
import pandas as pd
import re
import copy

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

        self.functionality = self.__init_functionality

        self.flat_time_x_agent_data = pd.read_csv(self.flat_time_x_agent_path_template.format(scenario_name))
        self.flat_time_x_environment_data = pd.read_csv(self.flat_time_x_environment_path_template.format(scenario_name))

        self.data_writer = DataWriter(output_file_suffix="with_statistics_{}".format(scenario_name))


    def __init_functionality(self):
        return \
            {
                'flat_time_x_agent':
                    {
                        "mean_square_error": self.__derive_statistics_flat_time_x_agent_mean_square_error,
                        "mean_absolute_error": self.__derive_statistics_flat_time_x_agent_mean_absolute_error,
                        "inlier_ratio": self.__derive_statistics_flat_time_x_agent_inlier_ratio
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
        pass  # PLACEHOLDER FOR FUTURE STATISTICS THAT ARE TIME AND ENVIRONMENT SPECIFIC

# ----------------------------------------------------------------------------------------------------------------------
# Supporting Methods Called by Main Functionality for Deriving Statistics and Measures Time and Agent Specific
# ----------------------------------------------------------------------------------------------------------------------

    def __derive_statistics_flat_time_x_agent_mean_square_error(self):
        # 1) read flat_time_x_environment WITH ERRORS ATTAchED file
        # 2) get measure per agent

        pass

    def __derive_statistics_flat_time_x_agent_mean_absolute_error(self):
        pass

    def __derive_statistics_flat_time_x_agent_inlier_ratio(self):
        pass

# ----------------------------------------------------------------------------------------------------------------------
# Supporting Methods Called by Main Functionality for Deriving Statistics and Measures Time and Environment Specific
# ----------------------------------------------------------------------------------------------------------------------

    def __derive_statistics_flat_time_x_environment_heatmap_errors(self):
        # define pattern to search for in column names
        regex = re.compile(r'(agent_\d*)')
        # 1) # get Column names
        column_names = copy.deepcopy(list(self.flat_time_x_environment_data.columns))
        # 2) list comprehension in combination with regex to find agent names
        agents = [re.findall(regex, column) for column in column_names]
        # 3) select only column that refer to an agent specific value
        agents = [column for column in agents if len(column) > 0]
        # 4) list comprehension fist instance of list in list is new list entry (re.findall returns a list with values)
        agents = [agent[0] for agent in agents]
        # 5) find only unique agents in columns
        agents = set(agents)
        agents = list(agents)
        # 6) loop over unique agents
        for agent in agents:
            # 7) Make Agent Error column with the real value (potential_catch) - predicted value (heatmap expectation)
            self.flat_time_x_environment_data['{}_environment_heatmap_error'.format(agent)] = \
                self.flat_time_x_environment_data['{}_catch_potential'.format(agent)] - \
                self.flat_time_x_environment_data['{}_catch_expectation_map'.format(agent)]

# ----------------------------------------------------------------------------------------------------------------------
# Supporting Methods Called by Main Functionality for Deriving Statistics and Measures in general
# ----------------------------------------------------------------------------------------------------------------------

    def __export_derivative_statistics_time_x_environment(self):
        self.data_writer.write_csv(self.flat_time_x_environment_data, 'flat_time_x_environment_results_with_statistics_')

    # EOF
