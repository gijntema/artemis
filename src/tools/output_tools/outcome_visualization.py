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
    01-09-2021

Version Number:
    0.1
"""


class GraphConstructor:

    # TODO: --STRUCTURAL-- expand dictionary library and migrate functionality of below methods
    def __init__(self): # piece of code if we want to make the methods below more flexible
        self.supported_dictionary_library = \
            {
                'bar': self.plot_bar_pandas,
                'line': self.plot_line_pandas
            }

# ----------------------------------------------------------------------------------------------------------------------
# Methods using a different way of plotting
# ----------------------------------------------------------------------------------------------------------------------

    def plot_bar_pandas(self, pd_dataframe, x_values, y_values=None, img_name='unnamed'):
        if y_values is None:
            y_values = list(pd_dataframe)                                                                               # if y values are not specified take all data series in the data
        fig = pd_dataframe.plot.bar(x=x_values, y=y_values)
        #fig.show()
        fig.write_image("{}.png".format(img_name))

    def plot_line_pandas(self, pd_dataframe, x_values, y_values=None, img_name='unnamed'):
        if y_values is None:
            y_values = list(pd_dataframe)                                                                               # if y values are not specified take all data series in the data
        fig = pd_dataframe.plot.line(x=x_values, y=y_values)
        fig.write_image("{}.png".format(img_name))
