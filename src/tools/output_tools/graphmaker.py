import copy

import pandas as pd
import os
import random
import matplotlib
import numpy as np
matplotlib.rcParams.update({'errorbar.capsize': 2})
#from mapping import scenario_map
import matplotlib.pyplot as plt

old_wd = os.getcwd()
os.chdir(old_wd.split('tools')[0] + 'output\\data_output')

class GraphMaker:

    def __init__(self, config_file):
        self.desired_graphs = []
        self.input_files = []
        self.functionality = self.__init_functionality()
        self.config_file = pd.read_csv(config_file)


    def __init_functionality(self):
        return \
            {
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

# Run File
# GraphMaker().sharing_x_avg_catch_y_nb_group_z()
starting_point = 101
end_point = 109
while end_point < 229:
    output_df = GraphMaker(config_file='C:\\Users\\ijnte001\\ARTEMIS\\src\\base_config_20211222.csv')\
        .time_x_ncorrect_heatmap_y_sharing_z(starting_point_csv_nb=starting_point,
                                                                 end_point=end_point)
    starting_point += 8
    end_point += 8

# EOF