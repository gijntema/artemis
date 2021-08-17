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
