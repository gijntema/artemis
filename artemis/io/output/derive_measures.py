# SEE BOTTOM FOR EXECUTION OF SCRIPT -- ALSO DEFINE PROPER SCENARIO FILE THERE

from artemis.io.output.export_data import DataWriter
import pandas as pd
import re
import copy
import os
import numpy as np
import statistics as stats

class MeasureDeriver:
    """Class to derive statistics and measures
    from two raw output data .csv files of ARTEMIS.py for a single run scenario"""
# ----------------------------------------------------------------------------------------------------------------------
# Initialisation Methods
# ----------------------------------------------------------------------------------------------------------------------

    def __init__(self,
                 scenario_name,
                 output_folder_name='output/data_output/',
                 flat_time_x_agent_file_name_template='flat_time_x_agent_results{}.csv',
                 flat_time_x_environment_file_name_template='flat_time_x_environment_results{}.csv',
                 inplace=True):

        self.flat_time_x_agent_path_template = output_folder_name + flat_time_x_agent_file_name_template
        self.flat_time_x_environment_path_template = output_folder_name + flat_time_x_environment_file_name_template

        self.functionality = self.__init_functionality()

        self.flat_time_x_agent_data = pd.read_csv(self.flat_time_x_agent_path_template.format(scenario_name))
        self.flat_time_x_environment_data = pd.read_csv(self.flat_time_x_environment_path_template.format(scenario_name))

        self.flat_time_x_environment_data['agents_visited'] = \
            self.flat_time_x_environment_data['agents_visited'].fillna('')                                              # convert nan values to empty strings to prevent bugging in later stages of the data analysis

        if not inplace:
            self.output_suffix = "_with_statistics_{}".format(scenario_name)
        else:
            self.output_suffix = scenario_name

        self.data_writer = DataWriter(output_file_suffix=self.output_suffix)


    def __init_functionality(self):
        return \
            {
                'flat_time_x_agent':
                    {
                        "mean_absolute_error": self.__derive_statistics_flat_time_x_agent_mean_absolute_error,
                        'mean_negative_error': self.__derive_statistics_flat_time_x_agent_mean_negative_error,
                        'mean_positive_error': self.__derive_statistics_flat_time_x_agent_mean_positive_error,
                        'sd_absolute_error': self.__derive_statistics_flat_time_x_agent_sd_absolute_error
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
        for statistics_deriver in self.functionality['flat_time_x_agent']:
            self.functionality['flat_time_x_agent'][statistics_deriver]()

    def derive_statistics_flat_time_x_environment(self):
        for statistics_deriver in self.functionality['flat_time_x_environment']:
            self.functionality['flat_time_x_environment'][statistics_deriver]()

# ----------------------------------------------------------------------------------------------------------------------
# Supporting Methods Called by Main Functionality for Deriving Statistics and Measures Time and Agent Specific
# ----------------------------------------------------------------------------------------------------------------------

    def __derive_statistics_flat_time_x_agent_mean_absolute_error(self):
        output_data = self.flat_time_x_agent_data
        data_series_mae = []

        # 0) get a list unique iterations, times and agents
        iterations = self.flat_time_x_environment_data['iteration_id'].unique()
        times = self.flat_time_x_environment_data['time_id'].unique()

        column_names = copy.deepcopy(list(self.flat_time_x_environment_data.columns))
        regex = re.compile(r'(agent_\d*)')
        agents = [re.findall(regex, column) for column in column_names]
        agents = [column for column in agents if len(column) > 0]
        agents = [agent[0] for agent in agents]
        agents = set(agents)
        agents = list(agents)
        agents.sort()

        # 1) for iteration in iterations
        for iteration in iterations:

            # 2) for time in times:
            for time in times:

                # 3) Take subset of iteration and time
                input_data = self.flat_time_x_environment_data[
                    (self.flat_time_x_environment_data['iteration_id'] == iteration) &
                    (self.flat_time_x_environment_data['time_id'] == time)]

                # 4) for agent in columns -- Ensure same order columns in environ and agent data sets
                for agent in agents:
                    # 5) take absolute values ==> data = [|x| for x in errors]
                    agent_errors = [abs(x) for x in input_data['{}_heatmap_error'.format(agent)]]

                    # 6) calculate mean avg(data)
                    mean_absolute_error = stats.mean(agent_errors)

                    # 7) attach to data series
                    data_series_mae.append(mean_absolute_error)

        # 8) attach data series to output pd.df
        output_data['mean_absolute_errors'] = data_series_mae

    def __derive_statistics_flat_time_x_agent_sd_absolute_error(self):
        output_data = self.flat_time_x_agent_data
        data_series_sdae = []

        # 0) get a list unique iterations, times and agents
        iterations = self.flat_time_x_environment_data['iteration_id'].unique()
        times = self.flat_time_x_environment_data['time_id'].unique()

        column_names = copy.deepcopy(list(self.flat_time_x_environment_data.columns))
        regex = re.compile(r'(agent_\d*)')
        agents = [re.findall(regex, column) for column in column_names]
        agents = [column for column in agents if len(column) > 0]
        agents = [agent[0] for agent in agents]
        agents = set(agents)
        agents = list(agents)
        agents.sort()

        # 1) for iteration in iterations
        for iteration in iterations:

            # 2) for time in times:
            for time in times:

                # 3) Take subset of iteration and time
                input_data = self.flat_time_x_environment_data[
                    (self.flat_time_x_environment_data['iteration_id'] == iteration) &
                    (self.flat_time_x_environment_data['time_id'] == time)]

                # 4) for agent in columns -- Ensure same order columns in environ and agent data sets
                for agent in agents:
                    # 5) take absolute values ==> data = [|x| for x in errors]
                    agent_errors = [abs(x) for x in input_data['{}_heatmap_error'.format(agent)]]

                    # 6) calculate mean avg(data)
                    sd_absolute_error = np.std(agent_errors)

                    # 7) attach to data series
                    data_series_sdae.append(sd_absolute_error)

        # 8) attach data series to output pd.df
        output_data['sd_absolute_errors'] = data_series_sdae

    def __derive_statistics_flat_time_x_agent_mean_positive_error(self):
        output_data = self.flat_time_x_agent_data
        data_series_mpe = []

        # 0) get a list unique iterations, times and agents
        iterations = self.flat_time_x_environment_data['iteration_id'].unique()
        times = self.flat_time_x_environment_data['time_id'].unique()

        column_names = copy.deepcopy(list(self.flat_time_x_environment_data.columns))
        regex = re.compile(r'(agent_\d*)')
        agents = [re.findall(regex, column) for column in column_names]
        agents = [column for column in agents if len(column) > 0]
        agents = [agent[0] for agent in agents]
        agents = set(agents)
        agents = list(agents)
        agents.sort()

        # 1) for iteration in iterations
        for iteration in iterations:

            # 2) for time in times:
            for time in times:

                # 3) Take subset of iteration and time
                input_data = self.flat_time_x_environment_data[
                    (self.flat_time_x_environment_data['iteration_id'] == iteration) &
                    (self.flat_time_x_environment_data['time_id'] == time)]

                # 4) for agent in columns -- Ensure same order columns in environ and agent data sets
                for agent in agents:
                    # 5) take only positive values ==> data = [|x| for x in errors]
                    agent_errors = [x for x in input_data['{}_heatmap_error'.format(agent)] if x >= 0]
                    if len(agent_errors) == 0:
                        agent_errors = [0]

                    # 6) calculate mean avg(data)
                    mean_positive_error = stats.mean(agent_errors)

                    # 7) attach to data series
                    data_series_mpe.append(mean_positive_error)

        # 8) attach data series to output pd.df
        output_data['mean_positive_errors'] = data_series_mpe

    def __derive_statistics_flat_time_x_agent_mean_negative_error(self):
        output_data = self.flat_time_x_agent_data
        data_series_mne = []

        # 0) get a list unique iterations, times and agents
        iterations = self.flat_time_x_environment_data['iteration_id'].unique()
        times = self.flat_time_x_environment_data['time_id'].unique()

        column_names = copy.deepcopy(list(self.flat_time_x_environment_data.columns))
        regex = re.compile(r'(agent_\d*)')
        agents = [re.findall(regex, column) for column in column_names]
        agents = [column for column in agents if len(column) > 0]
        agents = [agent[0] for agent in agents]
        agents = set(agents)
        agents = list(agents)
        agents.sort()

        # 1) for iteration in iterations
        for iteration in iterations:

            # 2) for time in times:
            for time in times:

                # 3) Take subset of iteration and time
                input_data = self.flat_time_x_environment_data[
                    (self.flat_time_x_environment_data['iteration_id'] == iteration) &
                    (self.flat_time_x_environment_data['time_id'] == time)]

                # 4) for agent in columns -- Ensure same order columns in environ and agent data sets
                for agent in agents:
                    # 5) take only positive values ==> data = [|x| for x in errors]
                    agent_errors = [x for x in input_data['{}_heatmap_error'.format(agent)] if x < 0]
                    if len(agent_errors) == 0:
                        agent_errors = [0]

                    # 6) calculate mean avg(data)
                    mean_negative_error = stats.mean(agent_errors)

                    # 7) attach to data series
                    data_series_mne.append(mean_negative_error)
        # 8) attach data series to output pd.df
        output_data['mean_negative_errors'] = data_series_mne
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

    def export_data(self):
        self.__export_derivative_statistics_time_x_environment()
        self.__export_derivative_statistics_time_x_agent()

    def __export_derivative_statistics_time_x_environment(self):
        self.data_writer.write_csv(self.flat_time_x_environment_data, 'flat_time_x_environment_results')

    def __export_derivative_statistics_time_x_agent(self):
        self.data_writer.write_csv(self.flat_time_x_agent_data, 'flat_time_x_agent_results')

# ----------------------------------------------------------------------------------------------------------------------
# EXECUTING THE SCRIPT
# ----------------------------------------------------------------------------------------------------------------------

# 0) set proper wd
old_dir = os.getcwd()
os.chdir(old_dir.removesuffix('\\tools\\output_tools'))

# 1) read scenario_file and get list of scenarios
scenario_file = 'base_config_20220218.csv'
suffix = scenario_file.split('.')[0].split('_')[-1]

output_folder_suffix = 'GI{}/'.format(suffix)                                                                           # determines that the output should be written to a subfolder in the regular output folder
# output_folder_suffix += 'GI{}'.format(suffix)

scenarios = pd.read_csv(scenario_file, sep=';')
scenarios = scenarios['scenario_id'].values
scenarios = np.unique(scenarios)


# 2) loop over scenarios
for scenario in scenarios:
    print('starting statistics for {}'.format(scenario))
    # 3) Initialise StatisticsDeriver for scenario (and read accompanying dat files)
    deriver = MeasureDeriver(scenario_name=scenario, output_folder_name='output/data_output/{}'.format(output_folder_suffix))

    # 4) Derive environment measures
    deriver.derive_statistics_flat_time_x_environment()

    # 5) derive agent measures
    deriver.derive_statistics_flat_time_x_agent()

    # 6?) others statistics
    # NA

    # 7) export data
    deriver.export_data()



# EOF
