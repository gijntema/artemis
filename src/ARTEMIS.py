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

# import internal modules
from src.config.init.init_param import *
from src.config.init.init_objects import ObjectInitializer
from src.run_model import ModelRunner
from src.tools.data_extraction import DataTransformer
from src.tools.outcome_visualization import GraphConstructor
from src.tools.export_data import DataWriter

# ensure the defined information sharing scenario is implemented
if information_sharing_scenario not in ['No Sharing',
                                        'Coalition Sharing',
                                        'Random Sharing']:

    raise NotImplementedError('Defined information sharing scenario not supported')

# initialize choice set and forager agents
object_initializer = ObjectInitializer()
choice_set = object_initializer.initialize_choice_set(choice_set_size, init_stock, sd_init_stock, growth_factor)
agent_set = object_initializer.initialize_forager_agents(amount_of_agents, choice_set,
                                                         catchability_coefficient, init_number_of_alternatives_known,
                                                         explore_probability, duration)

# RUN MODEL
model_runner = ModelRunner()
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

# transform the outcome objects of the model into usable data
data_transformer = DataTransformer()  # TODO identify functionality wanted in output data
alternative_specific_data, choice_set_time_series, agent_specific_data, agent_set_time_series = \
    data_transformer.transform_output_data(choice_set_output, agent_set_output, duration)


# produce graphical outputs
# TODO: adapt the GraphConstructor methods now that the data is already prepared through methods in DataTransformer
graph_constructor = GraphConstructor()
graph_constructor.make_graphs(agent_set=agent_set_output, choice_set=choice_set_output)

# produce database outputs (e.g. .csv or .json)
# TODO:  add functionality to export_data.py using methods for the DataWriter() object
