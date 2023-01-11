#
# This file is part of ARTEMIS (https://git.wur.nl/ecodyn/artemis.git).
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
This Module is aimed at making graphs from the output data of the ARTEMIS model,
as produced in by export_data.py in ARTEMIS.py and in ARTEMIS.py itself
The Module is currently an outdated version and needs to be updated

Module inputs:
-   None, but the module specifically only supports pandas.DataFrame objects

Module Usage:
-   the GraphConstructor objects are former inputs of ARTEMIS.py, old version needs t

Last Updated:
    01-10-2021

Version Number:
    0.1
"""

import copy
import pandas as pd
import os
import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import re
import seaborn as sns
from collections import defaultdict
matplotlib.rcParams.update({'errorbar.capsize': 2})


class GraphMaker:

    def __init__(self,
                 config_file,
                 data_folder_name='output/data_output/',
                 output_folder_name='output/data_output/graphs/',
                 flat_time_x_agent_file_name_template='flat_time_x_agent_results{}.csv',
                 flat_time_x_environment_file_name_template='flat_time_x_environment_results{}.csv'):

        self.config_file_name = config_file
        self.config_file = pd.read_csv(config_file, sep=';')
        self.functionality = self.__init_functionality()
        self.temp_data = ""

        #self.data_dictionary = self.__init_data_dictionary(flat_time_x_agent_file_name_template,
        #                                                   flat_time_x_environment_file_name_template)


    def __init_functionality(self):
        return {}#'errors': self.make_graph_erros_agent_012}

    def __init_data_dictionary(self,
                               flat_time_x_agent_file_name_template,
                               flat_time_x_environment_file_name_template):

        """reads and loads the data files that resulted form the ARTEMIS scenario runs as defined in the config_file"""
        data_dictionary = {}
        for scenario in self.config_file['scenario_id'].values:
            data_dictionary[scenario]['flat_time_x_agent_results'] = \
                pd.read_csv(flat_time_x_agent_file_name_template.format(scenario))
            data_dictionary[scenario]['flat_time_x_environment_results'] = \
                pd.read_csv(flat_time_x_environment_file_name_template.format(scenario))

        return data_dictionary

# ----------------------------------------------------------------------------------------------------------------------
# Methods for making graphs
# ----------------------------------------------------------------------------------------------------------------------

    def make_graph_time_x_MAE_NoC(self, scenarios=False):
        # 1) read config
        scenario_file = self.config_file
        if not scenarios:
            scenarios = scenario_file['scenario_id'].values
            scenarios = np.unique(scenarios)

        # 2) prepare data container pd.Dataframe
        constructed_data = pd.DataFrame()

        for scenario in scenarios:
            # 3) read data files (flat)
            scenario_data = pd.read_csv('output/data_output/flat_time_x_agent_results_with_statistics_{}.csv'.format(scenario))
            scenario_data = copy.deepcopy(scenario_data[scenario_data['agent_id'] == 'agent_012'])
            self.temp_data = scenario_data
            scenario_mae_data = copy.deepcopy(scenario_data['mean_absolute_errors'])

            constructed_data['mea_{}'.format(scenario)] = scenario_mae_data
            #constructed_data

        constructed_data['time_id'] = scenario_data['time_id']

        colours = ['black', 'blue', 'red', 'yellow', 'green']
        constructed_data.plot.line(x='time_id', subplots=True, color=colours)


    def make_graph_time_x_MPNE_NoC(self, scenarios=False):
        # 1) read config
        scenario_file = self.config_file
        if not scenarios:
            scenarios = scenario_file['scenario_id'].values
            scenarios = np.unique(scenarios)

        # 2) prepare data container pd.Dataframe
        constructed_data = pd.DataFrame()

        colours = ['black', 'black', 'blue', 'blue', 'red', 'red', 'green', 'green', 'yellow', 'yellow']
        for scenario in scenarios:
            # 3) read data files (flat)
            scenario_data = pd.read_csv('output/data_output/flat_time_x_agent_results_with_statistics_{}.csv'.format(scenario))
            scenario_data = copy.deepcopy(scenario_data[scenario_data['agent_id'] == 'agent_012'])
            self.temp_data = scenario_data
            scenario_mpe_data = copy.deepcopy(scenario_data['mean_positive_errors'])
            scenario_mne_data = copy.deepcopy(scenario_data['mean_negative_errors'])

            constructed_data['mpe_{}'.format(scenario)] = scenario_mpe_data
            constructed_data['mne_{}'.format(scenario)] = scenario_mne_data

        constructed_data['time_id'] = scenario_data['time_id']

        constructed_data.plot.line(x='time_id', subplots=True, color=colours)

    def make_graph_error_hist(self,  scenarios=False, times=[300]):

        # 1) read config
        scenario_file = self.config_file
        if not scenarios:
            scenarios = scenario_file['scenario_id'].values
            scenarios = np.unique(scenarios)


        # 2) prepare data container pd.Dataframe
        constructed_data = pd.DataFrame()

        for scenario in scenarios:
            # 3) read data files (flat)
            scenario_data = pd.read_csv('output/data_output/flat_time_x_environment_results_with_statistics_{}.csv'.format(scenario))
            for time in times:
                scenario_data_temp = copy.deepcopy(scenario_data[scenario_data['time_id'] == time])
                scenario_data_temp = copy.deepcopy(scenario_data_temp['agent_012_heatmap_error'])
                constructed_data['error_{}_{}'.format('t{}_'.format(time), scenario)] = copy.deepcopy(scenario_data_temp)

        colours = ['black', 'blue', 'red',  'green', 'yellow']
        constructed_data.plot.hist(bins=16, subplots=True, color=colours, range=(-32, 32))
        return constructed_data

    def make_graph_scatter(self, x, y, xlim, ylim, file_name, scenarios=False, start_time=0):

        # 1) read config
        scenario_file = self.config_file
        if not scenarios:
            scenarios = scenario_file['scenario_id'].values
            scenarios = np.unique(scenarios)

        for scenario in scenarios:
            colours = ['black', 'blue', 'red',  'green', 'yellow']
            colour_counter = 0
            # 2) prepare data container pd.Dataframe
            constructed_data_scenario = pd.DataFrame()

            # 3) read data files (flat)
            scenario_data = pd.read_csv('output/data_output/flat_time_x_{}_results_with_statistics_{}.csv'.format(file_name, scenario))
            scenario_data = scenario_data[scenario_data['time_id'] >= start_time]
            constructed_data_scenario = copy.deepcopy(scenario_data[[x, y]])

            fig = plt.figure()
            ax = plt.subplot(111)
            if xlim:
                ax.set_xlim(xlim)
            if ylim:
                ax.set_ylim(ylim)
            ax.set_title('scenario = {}'.format(scenario))

            constructed_data_scenario.plot(x=x, y=y,
                                           ax=ax, kind='scatter', c=colours[colour_counter])

            colour_counter += 1
            if colour_counter == len(colours):
                colour_counter -= len(colours)

    def make_graph_hist_general(self, series_name, file, scenarios=False, start_time=0):
        scenario_file = self.config_file

        constructed_data = pd.DataFrame()
        if not scenarios:
            scenarios = scenario_file['scenario_id'].values
            scenarios = np.unique(scenarios)

        for scenario in scenarios:
            scenario_data = pd.read_csv('output/data_output/flat_time_x_{}_results_with_statistics_{}.csv'.format(file, scenario))
            scenario_data = scenario_data[scenario_data['time_id'] >= start_time]

            scenario_data_temp = copy.deepcopy(scenario_data[series_name])
            constructed_data['{}_scen_{}_t=<{}'.format(series_name, scenario, start_time)] = scenario_data_temp

        colours = ['black', 'blue', 'red',  'green', 'yellow']
        constructed_data.plot.hist(bins=20, subplots=True, color=colours)

    def make_graph_hist_matrix_5D(self, file_name, data_subfolder, x_series_name, y_series_name, z_axis,
                                  multi_axis_I, multi_axis_II, z_tag, I_tag, II_tag,
                                  time_start, **scenario_selection_kwargs):
        """"please format kwargs as follows: series_name=[list of values to accept],
        Please note the kwargs make this method very flexible and accepting of many things that should not be accepted,
        so be careful when defining series filters in kwargs --INFLEXIBILITY STILL BUILT IN"""

        scenario_file = self.config_file
        selected_scenarios = copy.deepcopy(scenario_file)

        for series, values in scenario_selection_kwargs.items():
            # only select acceptable values for every defined series
            selected_scenarios = selected_scenarios[selected_scenarios[series].isin(values)]

        # make pandas DataFrame with relevant_values
        relevant_data = dict()
        x_short = x_series_name.split('|')[-1]
        y_short = y_series_name.split('|')[-1]

        for scenario in selected_scenarios['scenario_id'].values:
            scenario_data = pd.read_csv(
                'output/data_output/{}/flat_time_x_{}_results{}.csv'.format(
                    data_subfolder, file_name, scenario))
            scenario_data = scenario_data[scenario_data['time_id'] <= time_start]
            relevant_data[scenario] = pd.DataFrame()

            relevant_data[scenario]['{}_{}'.format(scenario, x_short)] = copy.deepcopy(scenario_data[x_series_name])
            relevant_data[scenario]['{}_{}'.format(scenario, y_short)] = copy.deepcopy(scenario_data[y_series_name])

            relevant_data[scenario]['{}_{}_bins'.format(scenario, x_short)] = \
                pd.cut(relevant_data[scenario]['{}_{}'.format(scenario, x_short)],
                       bins=[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200])

            graph_prepared_data = relevant_data[scenario].groupby('{}_{}_bins'.format(scenario, x_short), as_index=False)['{}_{}'.format(scenario, y_short)].mean()
            plot = graph_prepared_data.plot.bar(x='{}_{}_bins'.format(scenario, x_short), y='{}_{}'.format(scenario, y_short))

            plot.figure.savefig('{}.png'.format(scenario))

        # Quick and dirty fix

        #for value_I in selected_scenarios[multi_axis_I].unique():
        #    for value_II in selected_scenarios[multi_axis_II].unique():

    def make_graph_stock_expectation_boxplot(self, file_name, data_subfolder, y_series_name, x_series_name, time_start,
                                  **scenario_selection_kwargs):

        scenario_file = self.config_file
        selected_scenarios = copy.deepcopy(scenario_file)

        for series, values in scenario_selection_kwargs.items():
            # only select acceptable values for every defined series
            selected_scenarios = selected_scenarios[selected_scenarios[series].isin(values)]

        # make pandas DataFrame with relevant_values
        relevant_data = dict()
        x_short = x_series_name.split('|')[-1]
        y_short = y_series_name.split('|')[-1]

        for scenario in selected_scenarios['scenario_id'].values:
            # read scenario data
            scenario_data = pd.read_csv(
                'output/data_output/{}/flat_time_x_{}_results{}.csv'.format(
                    data_subfolder, file_name, scenario))
            scenario_data = scenario_data[scenario_data['time_id'] >= time_start]
            # prepare dataframe to build a graph from
            relevant_data[scenario] = pd.DataFrame()

            # get a single stock bins data series
            relevant_data[scenario]['{}_{}'.format(scenario, x_short)] = copy.deepcopy(scenario_data[x_series_name])
            relevant_data[scenario]['{}_{}_bins'.format(scenario, x_short)] = \
                pd.cut(relevant_data[scenario]['{}_{}'.format(scenario, x_short)],
                       bins=[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200])

            # find columns containing agents
            # 0) define pattern to search for in column names using regular expressions
            regex = re.compile(r'(agent_\d*)')

            # 1) # get Column names
            column_names = copy.deepcopy(list(scenario_data.columns))

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

            # loop over agent columns
            prepared_data = pd.DataFrame()
            for agent in agents:
                temp_data = pd.DataFrame()

                temp_data['{}_{}_bins'.format(scenario, x_short)] = copy.deepcopy(relevant_data[scenario]['{}_{}_bins'.format(scenario, x_short)])
                y_column_name = y_series_name.format(agent)
                temp_data['{}_{}'.format(scenario, y_short)] = copy.deepcopy(scenario_data[y_column_name])
                prepared_data = pd.concat([prepared_data, copy.deepcopy(temp_data)])

            # create boxplot
            plot = prepared_data.boxplot(column='{}_{}'.format(scenario, y_short),
                                            by='{}_{}_bins'.format(scenario, x_short))

            plot.figure.savefig('boxplots_{}.png'.format(scenario))

    def make_graph_stock_competition_boxplot(self, file_name, data_subfolder, y_series_name, x_series_name, time_start,
                                             **scenario_selection_kwargs):

        scenario_file = self.config_file
        selected_scenarios = copy.deepcopy(scenario_file)

        for series, values in scenario_selection_kwargs.items():
            # only select acceptable values for every defined series
            selected_scenarios = selected_scenarios[selected_scenarios[series].isin(values)]

        # make pandas DataFrame with relevant_values
        relevant_data = dict()
        x_short = x_series_name.split('|')[-1]
        y_short = y_series_name.split('|')[-1]

        for scenario in selected_scenarios['scenario_id'].values:
            # read scenario data
            scenario_data = pd.read_csv(
                'output/data_output/{}/flat_time_x_{}_results{}.csv'.format(
                    data_subfolder, file_name, scenario))
            scenario_data = scenario_data[scenario_data['time_id'] >= time_start]
            # prepare dataframe to build a graph from
            relevant_data[scenario] = pd.DataFrame()

            # get a single stock bins data series
            relevant_data[scenario]['{}_{}'.format(scenario, x_short)] = copy.deepcopy(scenario_data[x_series_name])
            relevant_data[scenario]['{}_{}_bins'.format(scenario, x_short)] = \
                pd.cut(relevant_data[scenario]['{}_{}'.format(scenario, x_short)],
                       bins=[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200])

            relevant_data[scenario]['{}_{}'.format(scenario, y_short)] = copy.deepcopy(scenario_data[y_series_name])

            prepared_data = copy.deepcopy(relevant_data[scenario])


            # create boxplot
            plot = prepared_data.boxplot(column='{}_{}'.format(scenario, y_short),
                                         by='{}_{}_bins'.format(scenario, x_short))

            plot.figure.savefig('boxplots_stock_competition_{}.png'.format(scenario))


    def make_graph_hist_cumulative_catch_per_agent(self, file_name, data_subfolder, time_start, x_bin_range, nb_bins,
                                                    **scenario_selection_kwargs):

        scenario_file = self.config_file
        selected_scenarios = copy.deepcopy(scenario_file)

        for series, values in scenario_selection_kwargs.items():
            # only select acceptable values for every defined series
            selected_scenarios = selected_scenarios[selected_scenarios[series].isin(values)]

        # make pandas DataFrame with relevant_values
        relevant_data = dict()
        #x_short = x_series_name.split('|')[-1]
        #y_short = y_series_name.split('|')[-1]

        for scenario in selected_scenarios['scenario_id'].values:
            # read scenario data
            scenario_data = pd.read_csv(
                'output/data_output/{}/flat_time_x_{}_results{}.csv'.format(
                    data_subfolder, file_name, scenario))
            scenario_data = scenario_data[scenario_data['time_id'] >= time_start]

            # prepare dataframe to build a graph from
            relevant_data[scenario] = copy.deepcopy(scenario_data[['agent_id', 'realised_catch']])
            relevant_data[scenario] = copy.deepcopy(relevant_data[scenario].groupby(['agent_id']).sum())
            relevant_data[scenario].rename(columns={'realised_catch': 'realised_catch_{}'.format(scenario)}, inplace=True)

            bins = []
            bin_counter = 0
            while bin_counter < nb_bins + 1:
                bins.append(x_bin_range[0] + ((x_bin_range[1] - x_bin_range[0])/nb_bins) * bin_counter)
                bin_counter += 1

            # make graph
            plot = relevant_data[scenario].plot.hist(by='realised_catch', bins=bins)
            plot.figure.savefig('cum_catch_hist_per_agent_{}.png'.format(scenario))

    def make_graph_hist_cumulative_catch_per_agent(self, file_name, data_subfolder, time_start, x_bin_range, nb_bins,
                                                   **scenario_selection_kwargs):

        scenario_file = self.config_file
        selected_scenarios = copy.deepcopy(scenario_file)

        for series, values in scenario_selection_kwargs.items():
            # only select acceptable values for every defined series
            selected_scenarios = selected_scenarios[selected_scenarios[series].isin(values)]

        # make pandas DataFrame with relevant_values
        relevant_data = dict()
        #x_short = x_series_name.split('|')[-1]
        #y_short = y_series_name.split('|')[-1]

        for scenario in selected_scenarios['scenario_id'].values:
            # read scenario data
            scenario_data = pd.read_csv(
                'output/data_output/{}/flat_time_x_{}_results{}.csv'.format(
                    data_subfolder, file_name, scenario))
            scenario_data = scenario_data[scenario_data['time_id'] >= time_start]

            # prepare dataframe to build a graph from
            relevant_data[scenario] = copy.deepcopy(scenario_data[['agent_id', 'realised_catch']])
            relevant_data[scenario] = copy.deepcopy(relevant_data[scenario].groupby(['agent_id']).sum())
            relevant_data[scenario].rename(columns={'realised_catch': 'realised_catch_{}'.format(scenario)}, inplace=True)

            bins = []
            bin_counter = 0
            while bin_counter < nb_bins + 1:
                bins.append(x_bin_range[0] + ((x_bin_range[1] - x_bin_range[0])/nb_bins) * bin_counter)
                bin_counter += 1

            # make graph
            plot = relevant_data[scenario].plot.hist(by='realised_catch', bins=bins)
            plot.figure.savefig('cum_catch_hist_per_agent_{}.png'.format(scenario))

    def make_graph_heat_inequility_on_bins(self, file_name, data_subfolder, time_start, x_name, y_name, nb_bins,
                                           xlabel, ylabel, **scenario_selection_kwargs):
        # access the scenario metadata
        scenario_file = self.config_file
        selected_scenarios = copy.deepcopy(scenario_file)

        # exclude scenarios we do not consider
        for series, values in scenario_selection_kwargs.items():
            # only select acceptable values for every defined series
            selected_scenarios = selected_scenarios[selected_scenarios[series].isin(values)]

        # prepare data containers
        relevant_data = defaultdict(list)
        index = []

        # consider all y_series values in order
        for y_value in scenario_selection_kwargs[y_name]:
            # save the y-axis value to use as index in a later stage
            index.append(str(y_value))

            # consider all x_series values in order
            for x_value in scenario_selection_kwargs[x_name]:

                # select a single scenario
                scenario = selected_scenarios[((selected_scenarios[y_name] == y_value) & (selected_scenarios[x_name] == x_value))]['scenario_id'].iloc[0]
                # load scenario data
                scenario_data = pd.read_csv(
                    'output/data_output/{}/flat_time_x_{}_results{}.csv'.format(
                        data_subfolder, file_name, scenario))

                scenario_data = scenario_data[scenario_data['time_id'] >= time_start]

                # calculate measure (mean catch of the highest bin - mean catch of the lowest bin)
                # 0) take only relevant data series
                temp_catch_data = copy.deepcopy(scenario_data[['agent_id', 'realised_catch']])

                # 1) take agents cumulative catch over all time steps per agent
                temp_catch_data = copy.deepcopy(temp_catch_data.groupby(['agent_id']).sum())

                # 2) assign catch bins
                temp_catch_data['catch_bins'] = pd.qcut(temp_catch_data['realised_catch'], q=nb_bins)

                # 3) group by bins and calculate average of bins
                temp_catch_data = copy.deepcopy(temp_catch_data.groupby(['catch_bins']).mean())

                # 4) highest bin - lowest bin
                catch_inequality = temp_catch_data['realised_catch'].max() - temp_catch_data['realised_catch'].min()

                # 5) save data point in the relevant_data dictionary in the column of x_value
                relevant_data[str(x_value)].append(catch_inequality)
                print("Inequality {} for x value {} and y value {}".format(catch_inequality, x_value, y_value))

        # prepare useable data format for plotting
        plot_df = pd.DataFrame(relevant_data, index=index).round(decimals=1)

        # plot data
        plot = sns.heatmap(plot_df, annot=True,
                           fmt='',
                           cbar_kws={'label': 'Difference in Average Cumulative Catch of the {}% highest and lowest'.format((1/nb_bins)*100)})
        plot.set_xlabel(xlabel)
        plot.set_ylabel(ylabel)
        plot.figure.savefig('inequality_bins_heatmap_{}.png'.format(self.config_file_name))

        return plot_df

    def make_graph_heat_inequility_on_bins_single_events(self, file_name, data_subfolder, time_start, x_name, y_name, nb_bins,
                                           xlabel, ylabel, **scenario_selection_kwargs):
        # access the scenario metadata
        scenario_file = self.config_file
        selected_scenarios = copy.deepcopy(scenario_file)

        # exclude scenarios we do not consider
        for series, values in scenario_selection_kwargs.items():
            # only select acceptable values for every defined series
            selected_scenarios = selected_scenarios[selected_scenarios[series].isin(values)]

        # prepare data containers
        relevant_data = defaultdict(list)
        index = []

        # consider all y_series values in order
        for y_value in scenario_selection_kwargs[y_name]:
            # save the y-axis value to use as index in a later stage
            index.append(str(y_value))

            # consider all x_series values in order
            for x_value in scenario_selection_kwargs[x_name]:

                # select a single scenario
                scenario = selected_scenarios[((selected_scenarios[y_name] == y_value) & (selected_scenarios[x_name] == x_value))]['scenario_id'].iloc[0]
                # load scenario data
                scenario_data = pd.read_csv(
                    'output/data_output/{}/flat_time_x_{}_results{}.csv'.format(
                        data_subfolder, file_name, scenario))

                scenario_data = scenario_data[scenario_data['time_id'] >= time_start]

                # calculate measure (mean catch of the highest bin - mean catch of the lowest bin)
                # 1) take only relevant data series
                temp_catch_data = copy.deepcopy(scenario_data[['agent_id', 'realised_catch']])

                # 2) assign catch bins
                temp_catch_data['catch_bins'] = pd.qcut(temp_catch_data['realised_catch'], q=nb_bins)

                # 3) group by bins and calculate average of bins
                temp_catch_data = copy.deepcopy(temp_catch_data.groupby(['catch_bins']).mean())

                # 4) highest bin - lowest bin
                catch_inequality = temp_catch_data['realised_catch'].max() - temp_catch_data['realised_catch'].min()

                # 5) save data point in the relevant_data dictionary in the column of x_value
                relevant_data[str(x_value)].append(catch_inequality)
                print("Inequality {} for x value {} and y value {}".format(catch_inequality, x_value, y_value))

        # prepare useable data format for plotting
        plot_df = pd.DataFrame(relevant_data, index=index).round(decimals=1)

        # plot data
        plot = sns.heatmap(plot_df, annot=True,
                           fmt='',
                           cbar_kws={'label': 'Difference in Average Catch of the {}% highest and lowest catch events'.format((1/nb_bins)*100)})
        plot.set_xlabel(xlabel)
        plot.set_ylabel(ylabel)
        plot.figure.savefig('inequality_bins_single_event_heatmap_{}.png'.format(self.config_file_name))

        return plot_df


#    def make_graph_heat_inequility_gini(self, file_name, data_subfolder, time_start, x_name, y_name,
#                                           xlabel, ylabel, **scenario_selection_kwargs):
#
#        # TODO: UNFINISHED AND UNIMPLEMENTED METHOD
#        # access the scenario metadata
#        scenario_file = self.config_file
#        selected_scenarios = copy.deepcopy(scenario_file)
#
#        # exclude scenarios we do not consider
#        for series, values in scenario_selection_kwargs.items():
#            # only select acceptable values for every defined series
#            selected_scenarios = selected_scenarios[selected_scenarios[series].isin(values)]

        # prepare data containers
#        relevant_data = defaultdict(list)
#        index = []

        # consider all y_series values in order
#        for y_value in scenario_selection_kwargs[y_name]:
#            # save the y-axis value to use as index in a later stage
#            index.append(str(y_value))

            # consider all x_series values in order
#            for x_value in scenario_selection_kwargs[x_name]:

                # select a single scenario
#                scenario = selected_scenarios[((selected_scenarios[y_name] == y_value) & (selected_scenarios[x_name] == x_value))]['scenario_id'].iloc[0]
                # load scenario data
#                scenario_data = pd.read_csv(
#                    'output/data_output/{}/flat_time_x_{}_results{}.csv'.format(
#                        data_subfolder, file_name, scenario))

#                scenario_data = scenario_data[scenario_data['time_id'] >= time_start]

                # calculate measure (mean catch of the highest bin - mean catch of the lowest bin)
                # 0) take only relevant data series
#                temp_catch_data = copy.deepcopy(scenario_data[['agent_id', 'realised_catch']])

                # 1) take agents cumulative catch over all time steps
#                temp_catch_data = copy.deepcopy(temp_catch_data.groupby(['agent_id']).sum())

                # 2) order catch list
#                temp_catch_data['ordered_catch'] = copy.deepcopy(temp_catch_data['realised_catch']).sort_values()

                # create cumulative list
#                temp_catch_data['cumulative_catch'] = [i +  for i in ]

                # 3) Calculate total
#                total_catch = temp_catch_data['ordered_catch'].sum()

                # 4) highest bin - lowest bin
#                catch_inequality = temp_catch_data['realised_catch'].max() - temp_catch_data['realised_catch'].min()

                # 5) save data point in the relevant_data dictionary in the column of x_value
#                relevant_data[str(x_value)].append(catch_inequality)
#                print("Inequality {} for x value {} and y value {}".format(catch_inequality, x_value, y_value))

        # prepare useable data format for plotting
#        plot_df = pd.DataFrame(relevant_data, index=index).round(decimals=1)

        # plot data
#        plot = sns.heatmap(plot_df, annot=True, fmt='',
#                           cbar_kws={'label': 'Difference in Average Cumulative Catch of the {} highest and lowest'})
#        plot.set_xlabel(xlabel)
#        plot.set_ylabel(ylabel)
#        plot.figure.savefig('inequality_bins_heatmap_{}.png'.format(self.config_file_name))

#        return plot_df



# ----------------------------------------------------------------------------------------------------------------------
# EXECUTING THE SCRIPT
# ----------------------------------------------------------------------------------------------------------------------

# set proper Working directory to folder 'src'
old_dir = os.getcwd()
os.chdir(old_dir.removesuffix('\\tools\\output_tools'))

# define folder where to find the result files in
data_subfolder = "GI20220412LastEventSharing"

# define form what time step onwards the data should be included
start_time = 400

# Initialise the graphmaker object
graph_maker = GraphMaker(config_file='base_config_20220412LastEventSharing.csv')

# define what values for three variables should be included
#comp_values = [1, 0.95, 0.8]            # the strength of competition
#share_values = [1]                      # the amount of sharing done
#Preset_values = [0.01, 0.1, 1]          # the chance the resource stocks change

comp_values = [1, 0.95, 0.9, 0.85, 0.8]            # the strength of competition
share_values = [1]                      # the amount of sharing done
Preset_values = [0.01, 0.1, 0.25, 0.33, 0.5, 0.66, 0.75, 0.9, 1]          # the chance the resource stocks change


#graph_maker.make_graph_hist_matrix_5D(file_name='environment', data_subfolder=data_subfolder, x_series_name='real_stock',
#                                      y_series_name='nb_agents_visited', z_axis='agents|sharing|sharing|nb_options_shared',
#                                      multi_axis_I='options|stock_reset|reset_probability',
#                                      multi_axis_II='competition|interference_attributes|interference_factor',
#                                      z_tag=None, I_tag=None,II_tag=None, time_start=400,
#                                      **{'agents|sharing|sharing|nb_options_shared': share_values,
#                                         'options|stock_reset|reset_probability': Preset_values,
#                                         'competition|interference_attributes|interference_factor': comp_values})

#graph_maker.make_graph_stock_expectation_boxplot(file_name='environment',
#                                                 data_subfolder=data_subfolder,
#                                                 x_series_name='real_stock',
#                                                 y_series_name='{}_catch_expectation_heatmap',
#                                                 time_start=start_time,
#                                                 **{'agents|sharing|sharing|nb_options_shared': share_values,
#                                                    'options|stock_reset|reset_probability': Preset_values,
#                                                    'competition|interference_attributes|interference_factor': comp_values})

#graph_maker.make_graph_stock_competition_boxplot(file_name='environment',
#                                                 data_subfolder=data_subfolder,
#                                                 x_series_name='real_stock',
#                                                 y_series_name='occurred_competition_correction',
#                                                 time_start=start_time,
#                                                 **{'agents|sharing|sharing|nb_options_shared': share_values,
#                                                    'options|stock_reset|reset_probability': Preset_values,
#                                                    'competition|interference_attributes|interference_factor': comp_values})

#graph_maker.make_graph_hist_cumulative_catch_per_agent(file_name='agent',
#                                                       data_subfolder=data_subfolder,
#                                                       time_start=start_time,
#                                                       x_bin_range=[0, 4000], nb_bins=40,
#                                                       **{'agents|sharing|sharing|nb_options_shared': share_values,
#                                                          'options|stock_reset|reset_probability': Preset_values,
#                                                          'competition|interference_attributes|interference_factor': comp_values})

#graph_maker.make_graph_hist_cumulative_catch_per_agent(file_name='agent',
#                                                       data_subfolder=data_subfolder,
#                                                       time_start=start_time,
#                                                       x_bin_range=[0, 4000], nb_bins=40,
#                                                       **{'agents|sharing|sharing|nb_options_shared': share_values,
#                                                          'options|stock_reset|reset_probability': Preset_values,
#                                                          'competition|interference_attributes|interference_factor': comp_values})

#graph_maker.make_graph_heat_inequility_on_bins(file_name='agent',
#                                               data_subfolder=data_subfolder,
#                                               time_start=start_time,
#                                               x_name='options|stock_reset|reset_probability',
#                                               y_name='competition|interference_attributes|interference_factor',
#                                               nb_bins=5,
#                                               ylabel='Competition Interference Factor',
#                                               xlabel="Reset Probability of the Resource Stock",
#                                               **{'agents|sharing|sharing|nb_options_shared': share_values,
#                                                  'options|stock_reset|reset_probability': Preset_values,
#                                                  'competition|interference_attributes|interference_factor': comp_values})

graph_maker.make_graph_heat_inequility_on_bins_single_events(file_name='agent',
                                                         data_subfolder=data_subfolder,
                                                         time_start=start_time,
                                                         x_name='options|stock_reset|reset_probability',
                                                         y_name='competition|interference_attributes|interference_factor',
                                                         nb_bins=5,
                                                         ylabel='Competition Interference Factor',
                                                         xlabel="Reset Probability of the Resource Stock",
                                                         **{'agents|sharing|sharing|nb_options_shared': share_values,
                                                            'options|stock_reset|reset_probability': Preset_values,
                                                            'competition|interference_attributes|interference_factor': comp_values})

# EOF