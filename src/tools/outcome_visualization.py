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

import matplotlib.pyplot as plt


class GraphConstructor:

    def __init__(self):
        self.supported_graphs = [] # piece of code if we want to make the methods below more flexible

# ----------------------------------------------------------------------------------------------------------------------
# Methods using a different way of plotting
# ----------------------------------------------------------------------------------------------------------------------
    def plot_bar_pandas(self, pd_dataframe, x_values, y_values=None):
        pd_dataframe.plot.bar(x=x_values, y=y_values)

    def plot_line_pandas(self, pd_dataframe, x_values, y_values=None):
        pd_dataframe.plot.line(x=x_values, y=y_values)