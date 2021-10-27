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

Module inputs:
-   None, but the module specifically only supports pandas.DataFrame objects

Module Usage:
-   the GraphConstructor objects are input for module ARTEMIS.py

Last Updated:
    01-10-2021

Version Number:
    0.1
"""

class GraphConstructor:

    # TODO: --STRUCTURAL-- expand dictionary library and migrate functionality of below methods
    def __init__(self, output_file_suffix=""):  # piece of code if we want to make the methods below more flexible
        self.output_file_suffix = output_file_suffix
        self.supported_dictionary_library = \
            {
                'bar': self.plot_bar_pandas,
                'line': self.plot_line_pandas
            }

# ----------------------------------------------------------------------------------------------------------------------
# Methods using a different way of plotting
# ----------------------------------------------------------------------------------------------------------------------

    def plot_bar_pandas(self, pd_dataframe, x_values, y_values=None, yerr_plus=None, yerr_min=None,
                        img_name='unnamed', y_label='value', legend_title='values'):
        if y_values is None:
            y_values = list(pd_dataframe)                                                                               # if y values are not specified take all data series in the data

        if yerr_plus is not None and yerr_min is not None:
            yerr_plus = pd_dataframe[yerr_plus]
            yerr_min = pd_dataframe[yerr_min]

        fig = pd_dataframe.plot.bar(x=x_values, y=y_values,
                                    error_y=yerr_plus,
                                    error_y_minus=yerr_min)
        fig.update_layout(yaxis_title=y_label,
                          legend_title=legend_title)

        # fig.show()                                                                                                    # line to immediatly show graphs, turned off for now
        fig.write_image("{}{}.png".format(img_name, self.output_file_suffix))

    def plot_line_pandas(self, pd_dataframe, x_values, y_values=None, yerr_plus=None, yerr_min=None,
                         img_name='unnamed', y_label='value', legend_title='values', y_range=False, x_range=False):
        if y_values is None:
            y_values = list(pd_dataframe)                                                                               # if y values are not specified take all data series in the data

        if yerr_plus is not None and yerr_min is not None:
            yerr_plus = pd_dataframe[yerr_plus]
            yerr_min = pd_dataframe[yerr_min]

        elif yerr_plus is not None and yerr_min is None:
            yerr_plus = pd_dataframe[yerr_plus]

        fig = pd_dataframe.plot.line(x=x_values, y=y_values,
                                     error_y=yerr_plus,
                                     error_y_minus=yerr_min)

        fig.update_layout(yaxis_title=y_label,
                          legend_title=legend_title)
        if y_range:
            fig.update_yaxes(range=y_range)
        if x_range:
            fig.update_xaxes(range=x_range)

        fig.write_image("{}{}.png".format(img_name, self.output_file_suffix))

    def plot_scatter_pandas(self, pd_dataframe, x_values, y_values, img_name='unnamed', y_range=False, x_range=False):
        fig = pd_dataframe.plot.scatter(x=x_values, y=y_values)

        if y_range:
            fig.update_yaxes(range=y_range)
        if x_range:
            fig.update_xaxes(range=x_range)

        fig.write_image("{}{}.png".format(img_name, self.output_file_suffix))


    def plot_jaccard(self, pd_dataframe, x_values, y_values=None, group_by=None,
                     img_name='unnamed', y_label='value', legend_title='values'):

        if y_values is None:
            y_values = list(pd_dataframe)

        fig = pd_dataframe.plot.bar(facet_row=group_by, x=x_values, y=y_values)

        fig.update_layout(yaxis_title=y_label,
                          legend_title=legend_title)

        # fig.show()                                                                                                      # line to immediatly show graphs, turned off for now
        fig.write_image("{}{}.png".format(img_name, self.output_file_suffix))
