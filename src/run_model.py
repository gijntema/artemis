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
import random


class ModelRunner:

    def __init__(self):
        pass

    def run_model(self, choice_set, agent_set, duration=10):
        agent_set = agent_set
        time_tracker = 0
        if isinstance(agent_set, int):
            raise TypeError("Agent_set is not an agent dictionary")
        agent_index_list = list(agent_set.keys())
        # loop for every time step
        while time_tracker < duration:
            random.shuffle(agent_index_list)            # shuffle agent order
            # loop for every agent
            for agent in agent_index_list:
                if random.random() > agent_set[agent].explore_probability:
                    alternative_index, catch = agent_set[agent].forage_maximalization('BASIC')
                else:
                    alternative_index, catch = agent_set[agent].forage_random(choice_set)

                agent_set[agent].update_agent_trackers(alternative_index=alternative_index, catch=catch)
            time_tracker += 1

        return choice_set, agent_set

