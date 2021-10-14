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

Last Updated:
    01-10-2021

Version Number:
    0.2
"""



# TODO: --MINOR-- replace 'alternatives' with 'choices' or 'options' in all variable, method and function nomenclature
# TODO: --STRUCTURAL-- Clean up Main Script

import timeit                                                                                                           # import module to track runtime

start = timeit.default_timer()                                                                                          # start timer for model run

# import internal modules
import pandas as pd                                                                                                     # pandas daytaframe as data structure tool
pd.options.plotting.backend = "plotly"                                                                                  # set a different, preffered over default,  style of plotting

# Other Modules in the ARTEMIS model
from src.config.init.init_param import *                                                                                # module containing parameter and scenario settings
from src.config.init.init_objects import ObjectInitializer                                                              # module to initialize the objects in the module (agents and choices)
from src.run_model import ModelRunner                                                                                   # module to run the model using initialized agents and choices
from src.tools.model_tools.competition import CompetitionHandler                                                        # module that handles model feedbacks as a result of competition between agents
from src.tools.output_tools.printing import PrintBlocker
from src.tools.output_tools.data_extraction import DataTransformer                                                      # module to generate output data from the objects in the model
from src.tools.output_tools.outcome_visualization import GraphConstructor                                               # module to make graphs from the output data
from src.tools.output_tools.export_data import DataWriter                                                               # module to write datafiles from the output data

print_blocker = PrintBlocker()
if reporting is not True:                                                                                               # block printing if desired
    print_blocker.block_print()

iteration_counter = 0                                                                                                   # initliazation of counter for iteration loops
alternative_specific_data = pd.DataFrame()                                                                              # intialize object to contain data on the choice options in the model
choice_set_time_series = pd.DataFrame()                                                                                 # intialize object to contain time series data on the choice options in the model
agent_specific_data = pd.DataFrame()                                                                                    # intialize object to contain data on the agents in the model
agent_set_time_series = pd.DataFrame()                                                                                  # intialize object to contain time series data on the agents in the model
other_x_catch_data = pd.DataFrame()                                                                                     # intialize object to contain a data series for catch and any desired otehr variable to correlate with catch

# initialize class objects that are part of operational structure
object_initializer = ObjectInitializer()                                                                                # initialize the object with the functionality to initialize agents and choice options
model_runner = ModelRunner()                                                                                            # initialize the object with the functionality to run a simulation with the initialized agents and choice options
competition_handler = CompetitionHandler(competition_method=competition_scenario)                                       # object that will ensure competition feedbacks are executed for in the model
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
    agent_set = object_initializer.initialize_forager_agents(nb_agents=number_of_agents,
                                                             choice_set=choice_set,                                     # initialize the forager agents in the model (e.g. fishermen)
                                                             catchability_coefficient=catchability_coefficient,
                                                             nb_alternatives_known=init_number_of_alternatives_known,
                                                             explore_probability=explore_probability,
                                                             duration_model=duration,
                                                             choice_method=choice_method
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
    alternative_specific_data = alternative_specific_data.append(temp_alternative_specific_data).reset_index(drop=True) # attach iteration specific choice option data to the full dataset and reset indices to prevent index errors -- Currently extracts final stock after a run and the cumulative number of catch events in each choice option
    choice_set_time_series = choice_set_time_series.append(temp_choice_set_time_series).reset_index(drop=True)          # attach iteration specific choice option time series data to the full dataset and reset indices to prevent index errors -- Currently no data series extracted, for future use
    agent_specific_data = agent_specific_data.append(temp_agent_specific_data).reset_index(drop=True)                   # attach iteration specific agent data to the full dataset and reset indices to prevent index errors -- Currently extracts the cumulative catch of an agent over a full simulation
    agent_set_time_series = agent_set_time_series.append(temp_agent_set_time_series).reset_index(drop=True)             # attach iteration specific agent time series data to the full dataset and reset indices to prevent index errors -- Currently extracts the total catch of all agents for every time st:>?

    other_x_catch_data = other_x_catch_data.append(data_transformer.get_other_x_catch(agent_set, iteration_counter)).reset_index(drop=True)  # Get desired explanatory variables x Catch dataframe

    iteration_counter += 1                                                                                              # progress to the next iteration

# ----------------------------------------------------------------------------------------------------------------------
# Get last simulation Explanatory Variables x Catch dataframe
# ----------------------------------------------------------------------------------------------------------------------


graph_constructor.plot_scatter_pandas(other_x_catch_data,
                                      x_values='average_expected_competitors', y_values="catch",
                                      img_name='competition_x_catch')

# ----------------------------------------------------------------------------------------------------------------------# Exit iteration loop and
# extract mean and sd from raw data outputs
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

avg_alternative_spec, avg_alternative_time, avg_agent_spec, avg_agent_time = \
    data_transformer.attach_sem_dataframes(
        alternative_specific_data, choice_set_time_series,
        agent_specific_data, agent_set_time_series,
        target_alt_spec=avg_alternative_spec, target_alt_time=avg_alternative_time,
        target_agent_spec=avg_agent_spec, target_agent_time=avg_agent_time)                                             # add Standard error of the mean (SEM) to dataframes

# ----------------------------------------------------------------------------------------------------------------------
# extract measures related to median and quantiles from raw data outputs
# ----------------------------------------------------------------------------------------------------------------------
# TODO: Migrate all stuff here to data_extraction.DataTransformer object
qt75_alternative_spec, qt75_alternative_time, qt75_agent_spec, qt75_agent_time = \
    data_transformer.get_qt_dataframes(alternative_specific_data,
                                       choice_set_time_series,
                                       agent_specific_data,
                                       agent_set_time_series, quantile=0.75)                                            # 75th quantile for four data types

qt50_alternative_spec, qt50_alternative_time, qt50_agent_spec, qt50_agent_time = \
    data_transformer.get_qt_dataframes(alternative_specific_data,
                                       choice_set_time_series,
                                       agent_specific_data,
                                       agent_set_time_series, quantile=0.50)                                            # 50th quantile AKA median

qt25_alternative_spec, qt25_alternative_time, qt25_agent_spec, qt25_agent_time = \
    data_transformer.get_qt_dataframes(alternative_specific_data,
                                       choice_set_time_series,
                                       agent_specific_data,
                                       agent_set_time_series, quantile=0.25)                                            # 25th quantile


qt_alternative_spec = qt25_alternative_spec\
    .join(qt50_alternative_spec.drop('alternative_id', axis='columns'), lsuffix='_qt25', rsuffix='_med')\
    .join(qt75_alternative_spec.drop('alternative_id', axis='columns').add_suffix('_qt75'))                             # merge 25th,50th and 75th into one dataframe for data contained in the DiscreteAlternative objects (AKA the option an agent can choose from)

qt_alternative_time = qt25_alternative_time \
    .join(qt50_alternative_time.drop('time_step_id', axis='columns'), lsuffix='_qt25', rsuffix='_med') \
    .join(qt75_alternative_time.drop('time_step_id', axis='columns').add_suffix('_qt75'))                               # merge 25th,50th and 75th into one dataframe for data contained in the ChoiceSet object (overarching data from trackers not specific to one DiscreteAlternative)

qt_agent_spec = qt25_agent_spec \
    .join(qt50_agent_spec.drop('agent_id', axis='columns'), lsuffix='_qt25', rsuffix='_med') \
    .join(qt75_agent_spec.drop('agent_id', axis='columns').add_suffix('_qt75'))                                         # merge 25th,50th and 75th into one dataframe for data contained in the ForagerAgent objects (AKA the specific behaviour and success of ForagerAgents)

qt_agent_time = qt25_agent_time \
    .join(qt50_agent_time.drop('time_step_id', axis='columns'), lsuffix='_qt25', rsuffix='_med') \
    .join(qt75_agent_time.drop('time_step_id', axis='columns').add_suffix('_qt75'))                                     # merge 25th,50th and 75th into one dataframe for data contained in the AgentSet objects (AKA the more general descriptors of fleets, flocks, packs or whatever group the agents represent)
# qt_agent_time['total_catch_err_min'] = \
#    abs(qt_agent_time['total_catch_med'] - qt_agent_time['total_catch_qt25'])                                          # add a column with the difference between the median and the 25th quantile
# qt_agent_time['total_catch_err_plus'] = \
#    abs(qt_agent_time['total_catch_med'] - qt_agent_time['total_catch_qt75'])                                          # add a column with the difference between teh median and the 75th quantile



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

graph_constructor.plot_bar_pandas(alternative_specific_data, x_values='alternative_id',
                                  y_values='alternative_final_stock',
                                  img_name='raw_alt_spec')                                                              # test to see distributions in the specific alternatives

# ----------------------------------------------------------------------------------------------------------------------
# produce graphical outputs - median and quantile values - ALL ERRORs currently needs to be fixed
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

# graph_constructor.plot_line_pandas(qt_agent_time, x_values='time_step_id',
#                                   y_values='total_catch_med',
#                                   yerr_plus='total_catch_err_plus',
#                                   yerr_min='total_catch_err_min',
#                                   img_name='qt_agent_time')                                                            # make line graph of the agent time series average data (plots the median cumulative catch an agent over time, with error bars to the 25th and 75th percentile

graph_constructor.plot_line_pandas(qt_agent_time, x_values='time_step_id', img_name= 'qt_agent_time')                   # make line graph of the choice option time series average data

# ----------------------------------------------------------------------------------------------------------------------
# produce data and graphical outputs - median, min and max values for memory evolution
# ----------------------------------------------------------------------------------------------------------------------

single_memory_data = data_transformer.get_single_simulation_memory_evolution(agent_set_output, duration)                # get data on the amount of options with an entry in the agents heatmap in the last simulation for every agent en time step specific

single_memory_data_summary = pd.DataFrame()                                                                             # make summary data for the memory evolution
single_memory_data_summary['time_step_id'] = single_memory_data['time_step_id']                                         # enter column with time
single_memory_data_summary['min_knowledge'] = single_memory_data.min(axis=1)                                            # enter column with the least knowledgeable agent value
single_memory_data_summary['med_knowledge'] = single_memory_data.median(axis=1)                                         # enter column with the median knowledgeable agent value
single_memory_data_summary['max_knowledge'] = single_memory_data.max(axis=1)                                            # enter column with the most knowledgeable agent value

graph_constructor.plot_line_pandas(single_memory_data, x_values='time_step_id',
                                   img_name='knowledge_evolution_last_simulation',
                                   y_label=' # of entries in heatmap', legend_title='Agents')                           # plot memory evolution over time fro all agents

graph_constructor.plot_line_pandas(single_memory_data_summary, x_values='time_step_id',
                                   img_name='summary_knowledge_evolution_last_simulation',
                                   y_label=' # of entries in heatmap', legend_title='Agents')                           # plot summary values for memory evolution over time (min-median-max

# ----------------------------------------------------------------------------------------------------------------------
# produce data and graphical outputs - intricate measure for the mean number of competitors (over all options) per agent
# ----------------------------------------------------------------------------------------------------------------------
competitor_df = data_transformer.extract_average_expected_competition(agent_set_output)                                 # make a pd.Dataframe from the data on the average amount of competitors in a given choice option
graph_constructor.plot_line_pandas(competitor_df,
                                   x_values='time_step_id', y_values=None,
                                   img_name='test_average_competitors_SA{}_SP{}_Pe%{}_J{}'.format(
                                                                                            shared_alternatives,      # format the img name with the number of memory entries (SA) shared with a number of people (SP) by every agent in every time step
                                                                                            share_partners,
                                                                                            int(
                                                                                                explore_probability
                                                                                                 * 100
                                                                                                ),
                                                                                            number_of_agents
                                                                                              ),
                                   y_label='average expected number of competitors'
                                   , legend_title='Agents')                                                             # make plot from data containgin data of agents average competitors per cell over time

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

data_writer.write_csv(single_memory_data, 'last_simulation_memory_evolution.csv')                                       # write knowledge evolution data


# jaccard_agent_knowledge = data_transformer.get_single_simulation_jaccard_matrices(agent_set_output)                     # get jaccard indices similarity matrices for last simulation
# data_writer.write_csv(jaccard_agent_knowledge, 'last_simulation_jaccard_agents.csv')
# data_writer.write_json(jaccard_agent_knowledge, 'last_simulation_jaccard_agents.json')
# graph_constructor.plot_jaccard(jaccard_agent_knowledge.drop('iteration_id', axis=1),
#                                x_values='agent_i',
#                                group_by='time_step_id',
#                                img_name='jaccard_agents',
#                                y_label='Jaccard Index Value',
#                                legend_title='agent_j')


# ----------------------------------------------------------------------------------------------------------------------
# Runtime tracking
# ----------------------------------------------------------------------------------------------------------------------
# check to see the knowledge an agent has at the end of the final simulation
for agent in agent_set_output.agents:                                                                                   # print the fill of each agents heatmap of the final simualtion
    print(agent, " knowns", "\t:\t", len(agent_set.agents[agent].list_of_known_alternatives))

print_blocker.enable_print()                                                                                            # enable printing to report on runtime and other prints that are always wanted

stop = timeit.default_timer()                                                                                           # stop model run timer
execution_time = stop - start                                                                                           # calculate occured runtime

print("Model Runtime: \t{} seconds".format(str(execution_time)))                                                        # report runtime in second
print('Average Yearly Catch of Final Simulation = {}'.format(str(agent_set_output.total_catch/duration)))
print('Average Yearly Catch over all Simulations = {}'.format(str(avg_agent_time['total_catch'].mean())))

