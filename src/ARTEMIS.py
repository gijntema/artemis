#
# This file is part of ARTEMIS (https://git.wur.nl/ecodyn/XXXX).
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

# import packages
import random
import numpy as np

# import internal modules
from src.config.init.init_param import *
from src.config.init.init_objects import ObjectInitializer
from src.run_model import ModelRunner

# initialize choice set and forager agents
object_initializer = ObjectInitializer()
choice_set = object_initializer.initialize_choice_set(choice_set_size, init_stock, sd_init_stock)
agent_set = object_initializer.initialize_forager_agents(amount_of_agents, choice_set,
                                                         catchability_coefficient, init_number_of_alternatives_known,
                                                         explore_probability)

# RUN MODEL
model_runner = ModelRunner()
choice_set_output, agent_set_output = model_runner.run_model(choice_set=choice_set,
                                                            agent_set=agent_set,
                                                            duration=duration)

# produce outputs
# do something with the results

