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

# TODO: replace 'alternatives' with 'choices' or 'options' in all variable, method and function nomenclature
# TODO: --MINOR-- Write consistent block comments and explanation at ALL classes and Methods in ALL modules
# TODO: --STRUCTURAL-- Clean up Main Script
# import module to track runtime
import timeit

start = timeit.default_timer()

# import internal modules
import pandas as pd
pd.options.plotting.backend = "plotly"

from src.config.init.init_param import *
from src.config.init.init_objects import ObjectInitializer
from src.run_model import ModelRunner
from src.tools.output_tools.data_extraction import DataTransformer
from src.tools.output_tools.outcome_visualization import GraphConstructor
from src.tools.output_tools.export_data import DataWriter

# TODO: -- MINOR -- Fix time_step naming as plotly does not recognise this well enough
iteration_counter = 0
alternative_specific_data = pd.DataFrame()
choice_set_time_series = pd.DataFrame()
agent_specific_data = pd.DataFrame()
agent_set_time_series = pd.DataFrame()

# initialize class objects that are part of operational structure
object_initializer = ObjectInitializer()
model_runner = ModelRunner()
data_transformer = DataTransformer()
graph_constructor = GraphConstructor()
data_writer = DataWriter()

while iteration_counter < number_of_iterations:
    print('-----------------------------------------------------------------------------------------------------------',
          '\nStarting Iteration no.{} \n'.format(str(iteration_counter)),
          "-----------------------------------------------------------------------------------------------------------"
          )
# ----------------------------------------------------------------------------------------------------------------------
# initialize choice set and forager agents
# ----------------------------------------------------------------------------------------------------------------------
    choice_set = object_initializer.initialize_choice_set(choice_set_size, init_stock, sd_init_stock, growth_factor)
    agent_set = object_initializer.initialize_forager_agents(amount_of_agents, choice_set,
                                                             catchability_coefficient,
                                                             init_number_of_alternatives_known,
                                                             explore_probability, duration, choice_method)

# ----------------------------------------------------------------------------------------------------------------------
# RUN SIMULATION
# ----------------------------------------------------------------------------------------------------------------------
    choice_set_output, agent_set_output = \
        model_runner.run_model(choice_set=choice_set,
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
    data_transformer = DataTransformer()  # TODO -- FUNCTIONALITY -- identify functionality wanted in output data
    temp_alternative_specific_data, \
    temp_choice_set_time_series, \
    temp_agent_specific_data, \
    temp_agent_set_time_series \
        = \
        data_transformer.transform_output_data(choice_set_output,
                                               agent_set_output,
                                               duration,
                                               iteration_id=iteration_counter)

    alternative_specific_data = alternative_specific_data.append(temp_alternative_specific_data).reset_index(drop=True)
    choice_set_time_series = choice_set_time_series.append(temp_choice_set_time_series).reset_index(drop=True)
    agent_specific_data = agent_specific_data.append(temp_agent_specific_data).reset_index(drop=True)
    agent_set_time_series = agent_set_time_series.append(temp_agent_set_time_series).reset_index(drop=True)

    iteration_counter += 1
# ----------------------------------------------------------------------------------------------------------------------
# Exit iteration loop and finish up
# ----------------------------------------------------------------------------------------------------------------------
avg_alternative_spec, avg_alternative_time, avg_agent_spec, avg_agent_time = \
    data_transformer.get_average_dataframes(alternative_specific_data,
                                            choice_set_time_series,
                                            agent_specific_data,
                                            agent_set_time_series)


# ----------------------------------------------------------------------------------------------------------------------
# produce graphical outputs
# ----------------------------------------------------------------------------------------------------------------------

graph_constructor.plot_bar_pandas(avg_alternative_spec, x_values='alternative_id', img_name='avg_alt_spec')
graph_constructor.plot_bar_pandas(avg_agent_spec, x_values='agent_id', img_name='avg_agent_spec')
graph_constructor.plot_line_pandas(avg_agent_time, x_values='time_step_id', img_name='avg_agent_time')
# graph_constructor.plot_line_pandas(avg_alternative_time, x_values='time_step_id', img_name = 'avg_alt_time')

# ----------------------------------------------------------------------------------------------------------------------
# produce database outputs (e.g. .csv or .json)
# ----------------------------------------------------------------------------------------------------------------------

data_writer.write_csv(alternative_specific_data, "alternative_data.csv")
data_writer.write_csv(choice_set_time_series, "choice_set_time_series.csv")
data_writer.write_csv(agent_specific_data, "agent_data.csv")
data_writer.write_csv(agent_set_time_series, "agent_set_time_series.csv")

data_writer.write_json(alternative_specific_data, "alternative_data.json")
data_writer.write_json(choice_set_time_series, "choice_set_time_series.json")
data_writer.write_json(agent_specific_data, "agent_data.json")
data_writer.write_json(agent_set_time_series, "agent_set_time_series.json")

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
stop = timeit.default_timer()
execution_time = stop - start

print("Model Runtime: \t{} seconds".format(str(execution_time)))  # returns time in second
