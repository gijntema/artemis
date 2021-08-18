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
import random


class ModelRunner:

    def __init__(self):
        pass

    def run_model(self,
                  choice_set,
                  agent_set,
                  information_sharing_scenario,
                  shared_alternatives,
                  share_partners,
                  duration=10,
                  stock_reset_scenario='no-reset',                      # default is a dynamics stock
                  init_stock=100,                                       # default if a non dynamic stock is 100 units
                  sd_init_stock=25):                                    # default sd if a non-dynamic stock is sd=25

        agent_index_list = list(agent_set.agents.keys())                # identify the id of every agent in a list
        # loop for every time step
        time_tracker = 0                                                # set a counter for time loops
        while time_tracker < duration:                                  # begin time loop
            print('---------------------------------------------------------------------------------------------------',
                  '\nStarting time step no.{} \n'.format(str(time_tracker)),
                  "---------------------------------------------------------------------------------------------------"
                  )
            random.shuffle(agent_index_list)                            # shuffle agent order for equal opportunities
            # loop for every agent
            for agent in agent_index_list:                              # begin loop for every agent

                # forage event occurs and agents choose an optimal or random alternative
                if random.random() > agent_set.agents[agent].explore_probability:          # optimalization using heatmap
                    alternative_index, catch = agent_set.agents[agent].forage_maximalization('BASIC', choice_set)

                else:                                                               # explore a random cell in the grid
                    alternative_index, catch = agent_set.agents[agent].forage_random(choice_set)

                # the stock in the chosen alternative is reduced and tracked using trackers
                # TODO: --STRUCTURAL-- Add functionality to scale catchability (and resulting catch) by effort
                # TODO: --STURCTURAL-- change quick and dirty fix one line below as parameter in init_param.py
                # choice_set.discrete_alternatives[alternative_index].resource_stock_harvest(catch)
                choice_set.catch_map[alternative_index] += catch
                choice_set.effort_map[alternative_index] += 1
                agent_set.update_agent_trackers(agent, catch, alternative_index, time_tracker)

                # operations specific to a sharing scenario
                if information_sharing_scenario == 'Random Sharing':
                    share_partner_counter = 0
                    while share_partner_counter < share_partners:
                        shared_heatmap_data = agent_set.agents[agent].share_heatmap_knowledge(
                            number_of_alternatives=shared_alternatives)
                        data_receiver_agent = random.choice(agent_index_list)
                        agent_set.agents[data_receiver_agent].receive_heatmap_knowledge(shared_heatmap_data)
                        print('{} is now sharing data on stock(s) in {} with {}'.format(str(agent), str(shared_heatmap_data[0]), str(data_receiver_agent)))
                        share_partner_counter += 1

            # growth of the resource stock
            for alternative in choice_set.discrete_alternatives:
                choice_set.discrete_alternatives[alternative].stock_growth()

            # reset the stocks if chosen for a static stock format - otherwise keep old stock
            if stock_reset_scenario == 'random-repeat':
                # TODO: --STRUCTURAL-- change hardcoded chance at stock reset/repetition to adaptable
                if random.random() < 0.9:                   # 90% chance of resetting the stock/10% chance at same stock
                    alternative_tracker = 0
                    nb_alternatives = len(choice_set.discrete_alternatives)
                    while alternative_tracker < nb_alternatives:
                        alternative_id = "alternative_" + str(alternative_tracker).zfill(4)
                        choice_set.discrete_alternatives[alternative_id].initialize_standard_stock(init_stock=init_stock,
                                                                                                   sd_init_stock=sd_init_stock)
                        alternative_tracker += 1

            time_tracker += 1                                           # proceed to the next time step

        return choice_set, agent_set

