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
This Module is used as the main execution of the model, it is divided into six core aspects:
- Initialize Parameters                         (import init_param.py)
- Initialize Model                              (make empty objects supporting structure of the model)
- Run Simulations                               (start iteration loop)
    -   Initialize model content                (Use init_objects.ObjectInitializer to set up options and agents in the iteration)
    -   Run Simulation                          (Use run_model.ModelRunner to run an iteration)
    -   extract output data to usable formats   (use DataTransformer to extract Pandas.Dataframe objects with raw data)
- Transform output data                         (Use DataTransformer to extract other measures, like averages)
- Export Data to datafiles                      (Use DataWriter to create .csv or .json files)
- Export data to figures                        (Use GraphConstructor to make graphs of the outcomes)

Module inputs:
-   almost all other modules are used directly or indirectly (through one of the other imported modules)

Module Usage:
-   Since this module is the Main, it is used to execute all other modules and is not used by other modules

"""



# TODO: Header What is the function this Script? maybe date, version number etc.

# TODO: --MINOR-- replace 'alternatives' with 'choices' or 'options' in all variable, method and function nomenclature
# TODO: --MINOR-- Write consistent block comments and explanation at ALL classes and Methods in ALL modules
# TODO: --STRUCTURAL-- Clean up Main Script

import timeit                                                                                                           # import module to track runtime

start = timeit.default_timer()                                                                                          # start timer for model run

# import internal modules
import pandas as pd                                                                                                     # pandas daytaframe as data structure tool
pd.options.plotting.backend = "plotly"                                                                                  # set a different, preffered over default,  style of plottting

from src.config.init.init_param import *                                                                                # module containing parameter and scenario settings
from src.config.init.init_objects import ObjectInitializer                                                              # module to initialize the objects in the module (agents and choices)
from src.run_model import ModelRunner                                                                                   # module to run the model using initialized agents and choices
from src.tools.output_tools.data_extraction import DataTransformer                                                      # module to generate output data from the objects in the model
from src.tools.output_tools.outcome_visualization import GraphConstructor                                               # module to make graphs from the output data
from src.tools.output_tools.export_data import DataWriter                                                               # module to write datafiles from the output data

# TODO: -- MINOR -- Fix time_step naming as plotly does not recognise this well enough
iteration_counter = 0                                                                                                   # initliazation of counter for iteration loop
alternative_specific_data = pd.DataFrame()                                                                              # intialize object to contain data on the choice options in the model
choice_set_time_series = pd.DataFrame()                                                                                 # intialize object to contain time series data on the choice options in the model
agent_specific_data = pd.DataFrame()                                                                                    # intialize object to contain data on the agents in the model
agent_set_time_series = pd.DataFrame()                                                                                  # intialize object to contain time series data on the agents in the model

# initialize class objects that are part of operational structure
object_initializer = ObjectInitializer()                                                                                # initialize the object with the functionality to initialize agents and choice options
model_runner = ModelRunner()                                                                                            # initialize the object with the functionality to run a simulation with the initialized agents and choice options
data_transformer = DataTransformer()                                                                                    # initialize the object with the functionality to extract output data from model objects
graph_constructor = GraphConstructor()                                                                                  # initialize the object with the functionality to make graphs from output data
data_writer = DataWriter()                                                                                              # initialize the object with the functionality to export data files from output data

while iteration_counter < number_of_iterations:
    print('-----------------------------------------------------------------------------------------------------------',# print statement for user to idnetify the progression of th emodel
          '\nStarting Iteration no.{} \n'.format(str(iteration_counter)),
          "-----------------------------------------------------------------------------------------------------------"
          )
# ----------------------------------------------------------------------------------------------------------------------
# initialize choice set and forager agents
# ----------------------------------------------------------------------------------------------------------------------
    choice_set = object_initializer.initialize_choice_set(choice_set_size, init_stock, sd_init_stock, growth_factor)    # initialize the potential option in the model (e.g. the grid with cells to fish in)
    agent_set = object_initializer.initialize_forager_agents(amount_of_agents, choice_set,                              # initialize the forager agents in the model (e.g. fishermen)
                                                             catchability_coefficient,
                                                             init_number_of_alternatives_known,
                                                             explore_probability, duration, choice_method)

# ----------------------------------------------------------------------------------------------------------------------
# RUN SIMULATION
# ----------------------------------------------------------------------------------------------------------------------
    choice_set_output, agent_set_output = \
        model_runner.run_model(choice_set=choice_set,                                                                   # run the model and return final states of the agents and choice options in the model
                               agent_set=agent_set,
                               duration=duration,
                               information_sharing_scenario=information_sharing_scenario,
                               share_partners=share_partners,
                               shared_alternatives=shared_alternatives,
                               stock_reset_scenario=stock_reset_scenario,
                               init_stock=init_stock,
                               sd_init_stock=sd_init_stock)

# ----------------------------------------------------------------------------------------------------------------------
# Transform the outcome objects of the model into usable data
# ----------------------------------------------------------------------------------------------------------------------
    # TODO -- FUNCTIONALITY -- identify functionality wanted in output data
    temp_alternative_specific_data, \
    temp_choice_set_time_series, \
    temp_agent_specific_data, \
    temp_agent_set_time_series \
        = \
        data_transformer.transform_output_data(choice_set_output,                                                       # extract four types of data from the output agents and choice options
                                               agent_set_output,
                                               duration,
                                               iteration_id=iteration_counter)
    # TODO: possible duplicate functionality in two different time series dataframes, might be merged
    alternative_specific_data = alternative_specific_data.append(temp_alternative_specific_data).reset_index(drop=True) # attach iteration specific choice option data to the full dataset and reset indices to prevent index errors
    choice_set_time_series = choice_set_time_series.append(temp_choice_set_time_series).reset_index(drop=True)          # attach iteration specific  choice option time series data to the full dataset and reset indices to prevent index errors
    agent_specific_data = agent_specific_data.append(temp_agent_specific_data).reset_index(drop=True)                   # attach iteration specific  agent data to the full dataset and reset indices to prevent index errors
    agent_set_time_series = agent_set_time_series.append(temp_agent_set_time_series).reset_index(drop=True)             # attach iteration specific  agent time series data to the full dataset and reset indices to prevent index errors

    iteration_counter += 1
# ----------------------------------------------------------------------------------------------------------------------
# Exit iteration loop and finish up
# ----------------------------------------------------------------------------------------------------------------------
avg_alternative_spec, avg_alternative_time, avg_agent_spec, avg_agent_time = \
    data_transformer.get_average_dataframes(alternative_specific_data,                                                  # extract averages from raw dataset with data from all iterations
                                            choice_set_time_series,
                                            agent_specific_data,
                                            agent_set_time_series)


# ----------------------------------------------------------------------------------------------------------------------
# produce graphical outputs
# ----------------------------------------------------------------------------------------------------------------------

graph_constructor.plot_bar_pandas(avg_alternative_spec, x_values='alternative_id', img_name='avg_alt_spec')             # make bar graph of the choice option specific average data
graph_constructor.plot_bar_pandas(avg_agent_spec, x_values='agent_id', img_name='avg_agent_spec')                       # make bar graph of the agent specific average data
graph_constructor.plot_line_pandas(avg_agent_time, x_values='time_step_id', img_name='avg_agent_time')                  # make line graph of the agent time series average data
# graph_constructor.plot_line_pandas(avg_alternative_time, x_values='time_step_id', img_name = 'avg_alt_time')          # make line graph of the choice option time series average data

# ----------------------------------------------------------------------------------------------------------------------
# produce database outputs (e.g. .csv or .json)
# ----------------------------------------------------------------------------------------------------------------------

data_writer.write_csv(alternative_specific_data, "alternative_data.csv")                                                # write raw, choice option data for each specific iteration to .csv file
data_writer.write_csv(choice_set_time_series, "choice_set_time_series.csv")                                             # write raw, choice option data for each specific iteration to .csv file
data_writer.write_csv(agent_specific_data, "agent_data.csv")                                                            # write raw, choice option data for each specific iteration to .csv file
data_writer.write_csv(agent_set_time_series, "agent_set_time_series.csv")                                               # write raw, choice option data for each specific iteration to .csv file

data_writer.write_json(alternative_specific_data, "alternative_data.json")                                              # write raw, choice option data for each specific iteration to .json file
data_writer.write_json(choice_set_time_series, "choice_set_time_series.json")                                           # write raw, choice option data for each specific iteration to .json file
data_writer.write_json(agent_specific_data, "agent_data.json")                                                          # write raw, choice option data for each specific iteration to .json file
data_writer.write_json(agent_set_time_series, "agent_set_time_series.json")                                             # write raw, choice option data for each specific iteration to .json file

# TODO: --FUNCTIONALITY-- Writing average data outcomes not supported yet (only templates given below)
# data_writer.write_json(alternative_specific_data, "average_alternative_data.json")
# data_writer.write_json(choice_set_time_series, "average_choice_set_time_series.json")
# data_writer.write_json(agent_specific_data, "average_agent_data.json")
# data_writer.write_json(agent_set_time_series, "average_choice_set_time_series.json")

# data_writer.write_csv(alternative_specific_data, "average_alternative_data.csv")
# data_writer.write_csv(choice_set_time_series, "average_choice_set_time_series.csv")
# data_writer.write_csv(agent_specific_data, "average_agent_data.csv")
# data_writer.write_csv(agent_set_time_series, "average_choice_set_time_series.csv")

# ----------------------------------------------------------------------------------------------------------------------
# Runtime tracking
# ----------------------------------------------------------------------------------------------------------------------
stop = timeit.default_timer()                                                                                           # stop model run timer
execution_time = stop - start                                                                                           # calculate occured runtime

print("Model Runtime: \t{} seconds".format(str(execution_time)))                                                        # report runtime in second
