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
import numpy as np
matplotlib.rcParams.update({'errorbar.capsize': 2})
#from mapping import scenario_map
import matplotlib.pyplot as plt


class GraphMaker:

    def __init__(self,
                 config_file,
                 data_folder_name='output/data_output/',
                 output_folder_name='output/data_output/graphs/',
                 flat_time_x_agent_file_name_template='flat_time_x_agent_results{}.csv',
                 flat_time_x_environment_file_name_template='flat_time_x_environment_results{}.csv'):

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

# ----------------------------------------------------------------------------------------------------------------------
# EXECUTING THE SCRIPT
# ----------------------------------------------------------------------------------------------------------------------

# set proper Working directory to folder 'src'
old_dir = os.getcwd()
os.chdir(old_dir.removesuffix('\\tools\\output_tools'))
considered_scenarios = ['2022_01_13_noC_s0', '2022_01_13_noC_s05', '2022_01_13_noC_s1', '2022_01_13_noC_s5','2022_01_13_noC_s10']
start_time = 200

graph_maker = GraphMaker(config_file='base_config_20220120.csv')
#graph_maker.make_graph_time_x_MAE_NoC(scenarios=considered_scenarios)
#graph_maker.make_graph_time_x_MPNE_NoC(scenarios=considered_scenarios)
#graph_maker.make_graph_error_hist(scenarios=considered_scenarios, times=[150])
#graph_maker.make_graph_error_hist(scenarios=considered_scenarios, times=[151])
#graph_maker.make_graph_error_hist(scenarios=considered_scenarios, times=[152])
graph_maker.make_graph_scatter(x='nb_agents_visited', y='real_stock', xlim=[0, 20], ylim=[0, 200],
                                     file_name='environment', scenarios=considered_scenarios, start_time=start_time)

graph_maker.make_graph_scatter(x='mean_absolute_errors', y='realised_catch', xlim=False, ylim=False,
                               file_name='agent', scenarios=considered_scenarios, start_time=start_time)

hist_env_meas = ['nb_agents_visited', 'occurred_competition_correction']
for data_series in hist_env_meas:
    graph_maker.make_graph_hist_general(series_name=data_series, file='environment', scenarios=considered_scenarios,
                                        start_time=start_time)

# ----------------------------------------------------------------------------------------------------------------------
# JUNK PARTS OF GraphMaker, MOVED TO CHILD CLASS OldGraphMaker
# ----------------------------------------------------------------------------------------------------------------------


class OldGraphMaker(GraphMaker):

    def __init__(self):
        GraphMaker.__init__(self)
        self.desired_graphs = []
        self.input_files = []
        self.functionality_old = self.__init_functionality_old()


    def __init_functionality_old(self):
        return {
            'Sharing X avg_catch+-sd X nb_groups': self.sharing_x_avg_catch_y_nb_group_z,
            'time X Ncorrect_heatmap X sharing': self.time_x_ncorrect_heatmap_y_sharing_z,
            'time X heatmap_correct_perception X sharing': self.time_x_heatmap_correct_perception_y_sharing_z
        }

    def add_input_files(self, list_of_file_names):

        if isinstance(list_of_file_names, str):
            list_of_file_names = [list_of_file_names]


    def sharing_x_avg_catch_y_nb_group_z(self):

        # make a list with csv, very quick and dirty and specific
        base_name = 'flat_time_x_agent_results{}.csv'
        list_of_csv = []
        csv_counter = 1
        while csv_counter < 38:
            list_of_csv.append(base_name.format('s{}'.format(str(csv_counter))))
            csv_counter += 1

        x_values = []
        y_values = []
        y_values_error = []
        z_values = []
        new_df = pd.DataFrame()
        for csv in list_of_csv:

            # read csv
            df = pd.read_csv(csv, sep=',')

            # X Axis Values
            # assess what sharing was, quick and dirty

            mapping = \
                {
                    base_name.format('s1'): 0.2,
                    base_name.format('s2'): 0,
                    base_name.format('s3'): 0.2,
                    base_name.format('s4'): 0.2,
                    base_name.format('s5'): 0.2,
                    base_name.format('s6'): 0.2,
                    base_name.format('s7'): 0.2,
                    base_name.format('s8'): 0.5,
                    base_name.format('s9'): 0.5,
                    base_name.format('s10'): 0.5,
                    base_name.format('s11'): 0.5,
                    base_name.format('s12'): 0.5,
                    base_name.format('s13'): 0.5,
                    base_name.format('s14'): 1,
                    base_name.format('s15'): 1,
                    base_name.format('s16'): 1,
                    base_name.format('s17'): 1,
                    base_name.format('s18'): 1,
                    base_name.format('s19'): 1,
                    base_name.format('s20'): 2,
                    base_name.format('s21'): 2,
                    base_name.format('s22'): 2,
                    base_name.format('s23'): 2,
                    base_name.format('s24'): 2,
                    base_name.format('s25'): 2,
                    base_name.format('s26'): 5,
                    base_name.format('s27'): 5,
                    base_name.format('s28'): 5,
                    base_name.format('s29'): 5,
                    base_name.format('s30'): 5,
                    base_name.format('s31'): 5,
                    base_name.format('s32'): 10,
                    base_name.format('s33'): 10,
                    base_name.format('s34'): 10,
                    base_name.format('s35'): 10,
                    base_name.format('s36'): 10,
                    base_name.format('s37'): 10,

                }

            sharing = mapping[csv]  # PLACEHOLDER
            x_values.append(sharing)

            # Y Axis Values
            avg_catch = df['catch'].mean()
            y_values.append(avg_catch)

            # Y Axis Error Values
            sd_catch = df['catch'].std()
            y_values_error.append(sd_catch)

            # Z Axis Values
            nb_groups = df['group_allegiance'].nunique()
            z_values.append(nb_groups)

        new_df['x'] = x_values
        new_df['y'] = y_values
        new_df['y_err'] = y_values_error
        new_df['z'] = z_values

        # plot
        ax = new_df.plot.scatter(x='x', xlabel='#sharing',
                                 y='y', ylabel='avg_catch_per agent', yerr='y_err',
                                 s=50, c='z', colormap='Accent_r')



    def time_x_ncorrect_heatmap_y_sharing_z(self, starting_point_csv_nb, end_point):
        base_name = 'GI20220103\\flat_time_x_agent_resultsS{}.csv'
        real_csv_counter = copy.deepcopy(starting_point_csv_nb)
        starting_point_csv_nb -= 100
        end_point -= 100
        list_of_csv = []
        relative_csv_counter = starting_point_csv_nb
        while relative_csv_counter < end_point:
            if ((relative_csv_counter + 8) % 8) % 3 == 1:
                list_of_csv.append(base_name.format('{}'.format(str(relative_csv_counter + 100))))
            relative_csv_counter += 1
            real_csv_counter += 1

        print(list_of_csv)
        x_values = []                       # Time
        y_values = []                       # Heatmap expected catch as % of real catch gained
        z_values = []                       # sharing frequency
        new_df = pd.DataFrame()

        # Mapping of share frequency to data file names - Quick and dirty for determining sharing frequency
        share_freq_mapping = \
            {
                '1': 0.1,
                '2': 0.2,
                '3': 0.5,
                '4': 1,
                '5': 2,
                '6': 5,
                '7': 10,
                '0': 20
            }

        interference_mapping = {}
        i = 1
        while i < 33:
            if i < 9:
                interference_mapping[str(i)] = 1
            elif 8 < i < 17:
                interference_mapping[str(i)] = 0.9
            elif 16 < i < 25:
                interference_mapping[str(i)] = 0.8
            else:
                interference_mapping[str(i)] = 0.7
            i += 1

        p_reset_mapping = {}
        i = 1
        while i < 129:
            if i < 33:
                p_reset_mapping[str(i)] = 0.1
            elif 32 < i < 65:
                p_reset_mapping[str(i)] = 0.2
            elif 64 < i < 97:
                p_reset_mapping[str(i)] = 0.3
            else:
                p_reset_mapping[str(i)] = 0.4
            i += 1

        for csv in list_of_csv:
            csv_counter = int(csv.split('resultsS')[1].split('.csv')[0]) - 100
            print(csv_counter)
            # read csv
            df = pd.read_csv(csv, sep=',')

            # pick random agent to follow for every scenario
            considered_agent = 'agent_012'

            # X Axis Values
            times = df['time_id'].unique()
            for time in times:
                x_values.append(time)

            # Y Axis Values
            agent_df = df[df['agent_id'] == considered_agent]
            for time in times:
                expected_catch = agent_df.iloc[time]['heatmap_expected_catch']
                real_uncorrected_catch = agent_df.iloc[time]['uncorrected_catch']
                correctness_of_chosen_entry = expected_catch / real_uncorrected_catch
                y_values.append(correctness_of_chosen_entry)

            # Z Axis Values
            # assess what sharing was, quick and dirty
            csv_key_sharing = str((csv_counter + 8) % 8)
            for time in times:
                sharing = share_freq_mapping[csv_key_sharing]
                z_values.append(sharing)

        new_df['x'] = x_values
        new_df['y'] = y_values
        new_df['z'] = z_values

        # title keys
        csv_key_interference = str(((relative_csv_counter + 32) % 32) - 1)
        csv_key_p_reset = str(relative_csv_counter-1)
        interference_title = interference_mapping[csv_key_interference]
        p_reset_title = p_reset_mapping[csv_key_p_reset]
        # nb_receiver_title =
        plot_title = 'Interference Factor = {} | P Reset Stock = {}'.format(interference_title, p_reset_title)
        file_title = 'time_x_logmismatch_y_sharing_z' + '_'.join(plot_title.split(' | ')) + '.png'
        # plot
        fig, ax = plt.subplots()

        new_df['logy'] = np.log(new_df['y'])

        for key, grp in new_df.groupby(['z']):
            ax = grp.plot(ax=ax, kind='line', x='x', y='logy',  label=key)
        plt.ylim(-4, 4)
        plt.xlim(25, 50)
        plt.xlabel('time')
        plt.ylabel('log heatmap expectation as % of real catch')
        plt.set_cmap('tab10')
        plt.title(plot_title)
        plt.savefig(file_title)
        return new_df

    def time_x_heatmap_correct_perception_y_sharing_z(self, starting_point_csv_nb, end_point):
        base_name = 'GI20211222\\flat_time_x_agent_resultsS{}.csv'
        starting_point_csv_nb -= 100
        end_point -= 100

# ----------------------------------------------------------------------------------------------------------------------
# Old Execution Script
# ----------------------------------------------------------------------------------------------------------------------


#starting_point = 101
#end_point = 109
#while end_point < 229:
#    output_df = GraphMaker(config_file='base_config_20211222.csv') \
#        .time_x_ncorrect_heatmap_y_sharing_z(starting_point_csv_nb=starting_point,
#                                             end_point=end_point)
#    starting_point += 8
#    end_point += 8

# EOF