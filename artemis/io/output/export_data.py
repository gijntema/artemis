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