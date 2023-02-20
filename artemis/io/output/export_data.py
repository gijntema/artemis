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
This Module is used to write model results to data files (e.g. .csv, .json)

All functionality is contained in methods and attributes of the DataWriter object

Module inputs:
-   any data formatted as pandas.DataFrame Object
-   the output data is defined and pre-processed in data_extraction.py to fit the prerequisites needed for this module

Module Usage:
-   ARTEMIS.py uses this module as Data writer

Last Updated:
    06-09-2021

Version Number:
    0.1
"""

import pandas as pd

class DataWriter:
    """contains a set of methods to export a pandas Dataframe object into output files (e.g. csv, json etc.)
    with a defined suffix text"""

# ----------------------------------------------------------------------------------------------------------------------
# Methods to initialise object
# ----------------------------------------------------------------------------------------------------------------------

    def __init__(self, output_file_suffix=""):
        self.output_file_suffix = output_file_suffix

# ----------------------------------------------------------------------------------------------------------------------
# Methods to write/export data files
# ----------------------------------------------------------------------------------------------------------------------

    def write_csv(self, pd_dataframe, filename):
        """writes data to a csv file in the output/data_output folder of the model directory, and naming the new file
        using a specified filename and a standard suffix"""

        if isinstance(pd_dataframe, pd.DataFrame) and isinstance(filename, str):
            file_path = "{}{}.csv".format(filename, self.output_file_suffix)                         # attach path to desired output folder
            pd_dataframe.to_csv(file_path)
        else:
            raise TypeError("Method only supports pandas.Dataframe objects as input and filename as strings")           # error handling: only pandas.Dataframes are accepted and only string filenames

    def write_json(self, pd_dataframe, filename):
        """writes data to a json file in the output/data_output folder of the model directory, and naming the new file
        using a specified filename and a standard suffix"""

        if isinstance(pd_dataframe, pd.DataFrame) and isinstance(filename, str):
            file_path = "{}{}.json".format(filename, self.output_file_suffix)                        # attach path to desired output folder
            pd_dataframe.to_json(file_path)
        else:
            raise TypeError("Method only supports pandas.Dataframe objects as input and filename as strings")           # error handling: only pandas.Dataframes are accepted and only string filenames

# EOF