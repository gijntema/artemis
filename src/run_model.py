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

        agent_index_list = list(agent_set.agents.keys())                # identify the id of every agent in a list
        # loop for every time step
        time_tracker = 0                                                # set a counter for time loops
        while time_tracker < duration:                                  # begin time loop
            random.shuffle(agent_index_list)                            # shuffle agent order for equal opportunities
            # loop for every agent
            for agent in agent_index_list:                              # begin loop for every agent

                # forage event occurs and agents choose an optimal or random alternative
                if random.random() > agent_set.agents[agent].explore_probability:          # optimalization using heatmap
                    alternative_index, catch = agent_set.agents[agent].forage_maximalization('BASIC', choice_set)

                else:                                                               # explore a random cell in the grid
                    alternative_index, catch = agent_set.agents[agent].forage_random(choice_set)

                # the stock in the chosen alternative is reduced and tracked using trackers
                choice_set.discrete_alternatives[alternative_index].resource_stock_harvest(catch)
                choice_set.catch_map[alternative_index] += catch
                choice_set.effort_map[alternative_index] += 1
                agent_set.update_agent_trackers(agent, catch, alternative_index, time_tracker)
            for alternative in choice_set.discrete_alternatives:
                choice_set.discrete_alternatives[alternative].stock_growth()

            time_tracker += 1                                           # proceed to the next time step

        return choice_set, agent_set

