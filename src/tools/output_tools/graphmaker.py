
import pandas as pd
import os
import matplotlib
matplotlib.rcParams.update({'errorbar.capsize': 2})
#from mapping import scenario_map

class GraphMaker:

    def __init__(self):
        self.desired_graphs = []
        self.input_files = []
        self.functionality = self.__init_functionality()


    def __init_functionality(self):
        return \
            {
                'Sharing X avg_catch+-sd X nb_groups': self.sharing_x_avg_catch_y_nb_group_z,
                'Sharing X avg_catch_within_group X nb_groups': None,
                'time X space fishing pressure': None,
                'sensitivity_to_volatility': None
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



# Run File
GraphMaker().sharing_x_avg_catch_y_nb_group_z()

# EOF