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

# from init_endogenous import *
# from init_param import *
from src.agents import ForagerAgent
from src.choice_set import ChoiceSet, DiscreteAlternative
import numpy as np


class ObjectInitializer:
    """class to initialize all objects for the model"""

    def __init__(self):
        pass

    def initialize_choice_set(self, nb_alternatives, init_stock, sd_init_stock):
        choice_set = ChoiceSet()
        alternative_tracker = 0
        while alternative_tracker < nb_alternatives:
            alternative_id = "alternative_" + str(alternative_tracker)
            choice_set.discrete_alternatives[alternative_id] = DiscreteAlternative()
            choice_set.discrete_alternatives[alternative_id].initialize_standard_stock(init_stock, sd_init_stock)
            alternative_tracker += 1

        return choice_set

    def initialize_forager_agents(self, nb_agents, choice_set, catchability_coeffcient, nb_alternatives_known, explore_probability):
        agent_set = {}
        agent_tracker = 0
        while agent_tracker < nb_agents:
            agent_id = 'agent_' + str(agent_tracker)
            agent_set[agent_id] = ForagerAgent()
            agent_set[agent_id].initialize_content(choice_set=choice_set,
                                                   agent_id=agent_id,
                                                   catchability_coefficient=catchability_coeffcient,
                                                   nb_of_alternatives_known=nb_alternatives_known,
                                                   explore_probability=explore_probability)

            agent_tracker += 1

        return agent_set
