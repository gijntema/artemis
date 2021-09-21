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

# TODO: Remember to check for bugging using Dictionary over OrderedDict (and consider collections.DefaultDict objects)
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

Last Updated:
    08-09-2021

Version Number:
    0.2
"""



# TODO: --MINOR-- replace 'alternatives' with 'choices' or 'options' in all variable, method and function nomenclature
# TODO: --STRUCTURAL-- Clean up Main Script

import timeit                                                                                                           # import module to track runtime

start = timeit.default_timer()                                                                                          # start timer for model run

# import internal modules
import pandas as pd                                                                                                     # pandas daytaframe as data structure tool
pd.options.plotting.backend = "plotly"                                                                                  # set a different, preffered over default,  style of plottting

# Other Modules in the ARTEMIS model
from src.config.init.init_param import *                                                                                # module containing parameter and scenario settings
from src.config.init.init_objects import ObjectInitializer                                                              # module to initialize the objects in the module (agents and choices)
from src.run_model import ModelRunner                                                                                   # module to run the model using initialized agents and choices
from src.tools.model_tools.competition import CompetitionHandler                                                        # module that handles model feedbacks as a result of competition between agents
from src.tools.output_tools.data_extraction import DataTransformer                                                      # module to generate output data from the objects in the model
from src.tools.output_tools.outcome_visualization import GraphConstructor                                               # module to make graphs from the output data
from src.tools.output_tools.export_data import DataWriter                                                               # module to write datafiles from the output data


# TODO: -- MINOR -- Fix time_step naming as plotly organises by first digit rather than full number
iteration_counter = 0                                                                                                   # initliazation of counter for iteration loops
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
competition_handler = CompetitionHandler(competition_method=competition_scenario)                                       # object that will ensure competition feedbacks are executed for in the model

while iteration_counter < number_of_iterations:
    print('-----------------------------------------------------------------------------------------------------------',# print statement for user to idnetify the progression of th emodel
          '\nStarting Iteration no.{} \n'.format(str(iteration_counter)),
          "-----------------------------------------------------------------------------------------------------------"
          )
# ----------------------------------------------------------------------------------------------------------------------
# initialize choice set and forager agents
# ----------------------------------------------------------------------------------------------------------------------
    choice_set = object_initializer.initialize_choice_set(choice_set_size, init_stock, sd_init_stock, growth_factor)    # initialize the potential option in the model (e.g. the grid with cells to fish in)
    agent_set = object_initializer.initialize_forager_agents(number_of_agents, choice_set,                              # initialize the forager agents in the model (e.g. fishermen)
                                                             catchability_coefficient,
                                                             init_number_of_alternatives_known,
                                                             explore_probability, duration, choice_method
                                                             )

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
                               sd_init_stock=sd_init_stock,
                               competition_handler=competition_handler,
                               stock_reset_chance=chance_reset_stock)

# ----------------------------------------------------------------------------------------------------------------------
# Transform the outcome objects of the model into usable data
# ----------------------------------------------------------------------------------------------------------------------
    # TODO -- FUNCTIONALITY -- identify functionality wanted in output data
    temp_alternative_specific_data, temp_choice_set_time_series, temp_agent_specific_data, temp_agent_set_time_series = \
        data_transformer.transform_output_data(choice_set_output,                                                       # extract four types of data from the output agents and choice options
                                               agent_set_output,
                                               duration,
                                               iteration_id=iteration_counter)

    # TODO: --MINOR-- possible duplicate functionality in two different time series dataframes, might be merged
    alternative_specific_data = alternative_specific_data.append(temp_alternative_specific_data).reset_index(drop=True) # attach iteration specific choice option data to the full dataset and reset indices to prevent index errors
    choice_set_time_series = choice_set_time_series.append(temp_choice_set_time_series).reset_index(drop=True)          # attach iteration specific  choice option time series data to the full dataset and reset indices to prevent index errors
    agent_specific_data = agent_specific_data.append(temp_agent_specific_data).reset_index(drop=True)                   # attach iteration specific  agent data to the full dataset and reset indices to prevent index errors
    agent_set_time_series = agent_set_time_series.append(temp_agent_set_time_series).reset_index(drop=True)             # attach iteration specific  agent time series data to the full dataset and reset indices to prevent index errors

    iteration_counter += 1                                                                                              # progress to the next iteration
# ----------------------------------------------------------------------------------------------------------------------
# Exit iteration loop and extract measures (e.g. mean of iterations) from raw data outputs
# ----------------------------------------------------------------------------------------------------------------------
avg_alternative_spec, avg_alternative_time, avg_agent_spec, avg_agent_time = \
    data_transformer.get_average_dataframes(alternative_specific_data,                                                  # extract averages from raw dataset with data from all iterations using methods from export_data.py functionality
                                            choice_set_time_series,
                                            agent_specific_data,
                                            agent_set_time_series)


# TODO: Make the underlying methods in DataTransformer more efficient, are all quick and dirty fixes now
sd_alternative_spec, sd_alternative_time, sd_agent_spec, sd_agent_time = \
    data_transformer.get_sd_dataframes(alternative_specific_data,                                                       # extract standard deviation from raw dataset with data from all iterations
                                        choice_set_time_series,
                                        agent_specific_data,
                                        agent_set_time_series)

qt75_alternative_spec, qt75_alternative_time, qt75_agent_spec, qt75_agent_time = \
    data_transformer.get_qt_dataframes(alternative_specific_data,
                                       choice_set_time_series,
                                       agent_specific_data,
                                       agent_set_time_series, quantile=0.75)

qt50_alternative_spec, qt50_alternative_time, qt50_agent_spec, qt50_agent_time = \
    data_transformer.get_qt_dataframes(alternative_specific_data,
                                       choice_set_time_series,
                                       agent_specific_data,
                                       agent_set_time_series, quantile=0.50)

qt25_alternative_spec, qt25_alternative_time, qt25_agent_spec, qt25_agent_time = \
    data_transformer.get_qt_dataframes(alternative_specific_data,
                                       choice_set_time_series,
                                       agent_specific_data,
                                       agent_set_time_series, quantile=0.25)


qt_alternative_spec = qt25_alternative_spec\
    .join(qt50_alternative_spec.drop('alternative_id', axis='columns'), lsuffix='_qt25', rsuffix='_med')\
    .join(qt75_alternative_spec.drop('alternative_id', axis='columns').add_suffix('_qt75'))

qt_alternative_time = qt25_alternative_time \
    .join(qt50_alternative_time.drop('time_step_id', axis='columns'), lsuffix='_qt25', rsuffix='_med') \
    .join(qt75_alternative_time.drop('time_step_id', axis='columns').add_suffix('_qt75'))

qt_agent_spec = qt25_agent_spec \
    .join(qt50_agent_spec.drop('agent_id', axis='columns'), lsuffix='_qt25', rsuffix='_med') \
    .join(qt75_agent_spec.drop('agent_id', axis='columns').add_suffix('_qt75'))

qt_agent_time = qt25_agent_time \
    .join(qt50_agent_time.drop('time_step_id', axis='columns'), lsuffix='_qt25', rsuffix='_med') \
    .join(qt75_agent_time.drop('time_step_id', axis='columns').add_suffix('_qt75'))
qt_agent_time['total_catch_err_min'] = \
    abs(qt_agent_time['total_catch_med'] - qt_agent_time['total_catch_qt25'])
qt_agent_time['total_catch_err_plus'] = \
    abs(qt_agent_time['total_catch_med'] - qt_agent_time['total_catch_qt75'])


avg_alternative_spec, avg_alternative_time, avg_agent_spec, avg_agent_time = \
    data_transformer.attach_sem_dataframes(
        alternative_specific_data, choice_set_time_series,
        agent_specific_data, agent_set_time_series,
        target_alt_spec=avg_alternative_spec, target_alt_time=avg_alternative_time,
        target_agent_spec=avg_agent_spec, target_agent_time=avg_agent_time)


# TODO: TODO create files with raw data:catch per agent per time step (1 iteration)
#  not averaged over the number of simulations - data found below after graphical outputs (currently line 164+)

# ----------------------------------------------------------------------------------------------------------------------
# produce graphical outputs - average values
# ----------------------------------------------------------------------------------------------------------------------

graph_constructor.plot_bar_pandas(avg_alternative_spec, x_values='alternative_id', img_name='avg_alt_spec')             # make bar graph of the choice option specific average data
graph_constructor.plot_bar_pandas(avg_agent_spec, x_values='agent_id', img_name='avg_agent_spec')                       # make bar graph of the agent specific average data

graph_constructor.plot_line_pandas(avg_agent_time, x_values='time_step_id',
                                   y_values='total_catch', yerr_plus='total_catch_sem',
                                   img_name='avg_agent_time')                                                           # make line graph of the agent time series average data

# graph_constructor.plot_line_pandas(avg_alternative_time, x_values='time_step_id', img_name = 'avg_alt_time')          # make line graph of the choice option time series average data

graph_constructor.plot_bar_pandas(alternative_specific_data, x_values='alternative_id', y_values='alternative_effort',
                                  img_name='raw_alt_spec')                                                              # test to see distributions in the specific alternatives

# ----------------------------------------------------------------------------------------------------------------------
# produce graphical outputs - median and quantile values
# ----------------------------------------------------------------------------------------------------------------------

# ERROR Code, needs to be fixed, quick and dirty fixes below
# graph_constructor.plot_bar_pandas(qt_alternative_spec, x_values='alternative_id',
#                                  y_values=[col for col in qt_alternative_spec.columns if 'med' in col],
#                                  yerr_plus=[col for col in qt_alternative_spec.columns if 'qt75' in col],
#                                  yerr_min=[col for col in qt_alternative_spec.columns if 'qt25' in col],
#                                  img_name='qt_alt_spec')                                                               # make bar graph of the choice option specific average data

# graph_constructor.plot_bar_pandas(qt_agent_spec, x_values='agent_id',
#                                  y_values=[col for col in qt_alternative_spec.columns if 'med' in col],
#                                  yerr_plus=[col for col in qt_alternative_spec.columns if 'qt75' in col],
#                                  yerr_min=[col for col in qt_alternative_spec.columns if 'qt25' in col],
#                                  img_name='qt_agent_spec')                                                             # make bar graph of the agent specific average data

graph_constructor.plot_line_pandas(qt_agent_time, x_values='time_step_id',
                                   y_values='total_catch_med',
                                   yerr_plus='total_catch_err_plus',
                                   yerr_min='total_catch_err_min',
                                   img_name='qt_agent_time')                                                            # make line graph of the agent time series average data

# graph_constructor.plot_line_pandas(qt_alternative_time, x_values='time_step_id', img_name = 'qt_alt_time')            # make line graph of the choice option time series average data


# ----------------------------------------------------------------------------------------------------------------------
# produce database outputs (e.g. .csv or .json)
# ----------------------------------------------------------------------------------------------------------------------

data_writer.write_csv(alternative_specific_data, "alternative_data.csv")                                                # write raw, choice option data for each specific iteration to .csv file
data_writer.write_csv(choice_set_time_series, "choice_set_time_series.csv")                                             # write raw, choice option data for each specific iteration to .csv file
data_writer.write_csv(agent_specific_data, "agent_data.csv")                                                            # write raw, agent data for each specific iteration to .csv file
data_writer.write_csv(agent_set_time_series, "agent_set_time_series.csv")                                               # write raw, agent data for each specific iteration to .csv file

data_writer.write_json(alternative_specific_data, "alternative_data.json")                                              # write raw, choice option data for each specific iteration to .json file
data_writer.write_json(choice_set_time_series, "choice_set_time_series.json")                                           # write raw, choice option data for each specific iteration to .json file
data_writer.write_json(agent_specific_data, "agent_data.json")                                                          # write raw, agent data for each specific iteration to .json file
data_writer.write_json(agent_set_time_series, "agent_set_time_series.json")                                             # write raw, agent data for each specific iteration to .json file

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
print('Average Yearly Catch of Final Simulation = {}'.format(str(agent_set_output.total_catch/duration)))
print('Average Yearly Catch = {}'.format(str(avg_agent_time['total_catch'].mean())))

# check to see the knowledge an agent has at the end of the final simulation
for agent in agent_set.agents:
    print(agent, " knowns", "\t:\t", len(agent_set.agents[agent].list_of_known_alternatives))