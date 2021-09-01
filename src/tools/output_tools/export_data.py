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

Module Usage:
-   ARTEMIS.py uses this module as Data writer

Last Updated:
    01-09-2021

Version Number:
    0.1
"""

import pandas as pd

class DataWriter:
    """contains a set of methods to transform a pandas Dataframe object into output files"""

    def write_csv(self, pd_dataframe, filename):
        if isinstance(pd_dataframe, pd.DataFrame) and isinstance(filename, str):
            file_path = "output/data_output/" + filename
            pd_dataframe.to_csv(file_path)
        else:
            raise TypeError("Method only supports pandas.Dataframe objects as input and filename as strings")

    def write_json(self, pd_dataframe, filename):
        if isinstance(pd_dataframe, pd.DataFrame) and isinstance(filename, str):
            file_path = "output/data_output/" + filename
            pd_dataframe.to_json(file_path)
        else:
            raise TypeError("Method only supports pandas.Dataframe objects as input and filename as strings")
