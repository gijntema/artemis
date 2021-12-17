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


"""Module that runs a simulation based on objects initialised in ARTEMIS.py using init_objects.py

Module inputs:
-   No explicit inputs, but the module uses Objects created by agents.py and choice_set.py extensively

Module Usage:
-   module is used by ARTEMIS.py

Last Updated:
01-10-2021

Version Number:
0.2
"""

import random


class ModelRunner:

    def __init__(self):
        pass

    def run_model(self,
                  choice_set,                                           # the choice options in the model
                  fleet,                                            # the agents in the model
                  duration=10,                                          # duration of the model (no. time steps)
                  stock_reset_scenario='no-reset',                      # default is a non dynamics stock
                  init_stock=100,                                       # default if a non dynamic stock is 100 units
                  sd_init_stock=25,                                     # default sd if a non-dynamic stock is sd=25
                  competition_handler=None,                             # object that ensures the effects of competition are implemented
                  stock_reset_chance=0.9,                               # the chance at the stock being reset to default initialisation (mean +-sd)
                  iteration_id=-99,                                     # for reporting on iterations
                  min_stock=0,
                  max_stock=100):

        agent_index_list = list(fleet.agents.keys())                # identify the id of every agent in a list

        # loop for every time step
        time_tracker = 0                                                # set a counter for time loops
        while time_tracker < duration:                                  # begin time loop
            print('---------------------------------------------------------------------------------------------------',
                  '\nStarting time step no.{} in iteration no. {}\n'.format(str(time_tracker), iteration_id),
                  "---------------------------------------------------------------------------------------------------"
                  )
            time_id = str(time_tracker).zfill(len(str(duration)))
            random.shuffle(agent_index_list)                                                                            # shuffle agent order for equal opportunities
            fleet.update_memory_trackers(time_id)                                                                   # record knowledge on the choice options at the start of a time period
            fleet.update_average_expected_competitor_tracker(time_id)                                               # update tracker for the expected amount of competitors

            # loop for every agent
            for agent in agent_index_list:                                                                              # begin choice loop for every agent

                # forage event occurs and agents choose an optimal or random alternative
                alternative_index = fleet.agents[agent].make_choice(choice_set)
                fleet.update_forage_visit_tracker(time_id=time_id,
                                                     agent_id=agent,
                                                     chosen_alternative=alternative_index)                              # update the tracker that keeps track of where agents have gone to: TODO: QUICK and DIRTY implemented fo rnow

                # load the expected catch in the chosen location to the fleet tracker
                fleet.update_heatmap_expectation_tracker(time_id=time_id, agent_id=agent,
                                                         expected_catch=fleet.agents[agent].heatmap[alternative_index])

                # load the chosen alternative to the object that will introduce competition between agents
                competition_handler.load_competition_data(alternative_index, agent)

            for agent in agent_index_list:                                                                              # Second agent loop to execute choices --> second loop is needed to account for competition
                # Catch is corrected for competition effects and trackers are updated
                # if harvest removal is on, the stock is also reduced
                competition_handler.competition_correction(choice_set, fleet, agent, time_id=time_id)

                # share data with other agent(s)
                fleet.agents[agent].heatmap_exchanger.provide_data(fleet)

            # growth of the resource stock
            for alternative in choice_set.discrete_alternatives:                                                        # loop over all choice options to allow resource stock growth
                choice_set.discrete_alternatives[alternative].stock_growth()

            # reset the stocks if chosen for a static stock format - otherwise keep old stock
            # TODO: migrate if-statement functionality to library dictionary with functions for flexibility
            if stock_reset_scenario == 'normal_random_repeat':                                                          # if statement for repeating stocks
                alternative_tracker = 0                                                                                 # initialise counter for loop functionality
                nb_alternatives = len(choice_set.discrete_alternatives)                                                 # extract a list of choice option IDs
                while alternative_tracker < nb_alternatives:                                                            # Loop over all choice options
                    if random.random() < stock_reset_chance:                                                            # if a random number between 0 and 1 is below the stock reset chance, we reset the stock
                        alternative_id = "alternative_" + str(alternative_tracker).zfill(len(str(nb_alternatives)))     # transform counter variable into actual choice option ID.
                        choice_set.discrete_alternatives[alternative_id].\
                            initialize_standard_stock(init_stock=init_stock, sd_init_stock=sd_init_stock,
                                                      stock_distribution=stock_reset_scenario)                          # reinitialise stock drawn from a normal distribution with goven mean and init stock
                    alternative_tracker += 1                                                                            # proceed to next choice option

            elif stock_reset_scenario == 'uniform_random_repeat':                                                       # if statement for repeating stocks
                alternative_tracker = 0                                                                                 # initialise counter for loop functionality
                nb_alternatives = len(choice_set.discrete_alternatives)                                                 # extract a list of choice option IDs
                while alternative_tracker < nb_alternatives:                                                            # Loop over all choice options
                    if random.random() < stock_reset_chance:                                                            # if a random number between 0 and 1 is below the stock reset chance, we reset the stock
                        alternative_id = "alternative_" + str(alternative_tracker).zfill(len(str(nb_alternatives)))     # transform counter variable into actual choice option ID.
                        choice_set.discrete_alternatives[alternative_id].\
                            init_uniform_standard_stock(max_stock, min_stock)                                           # reinitialise stock drawn from uniform distribution with given max and and min stock
                    alternative_tracker += 1

            competition_handler.reset_relevant_data()                                                                   # ensure the competition_handler is reset to default to start next time_step fresh
            time_tracker += 1                                                                                           # proceed to the next time step

        return choice_set, fleet                                                                                        # return the final choice options and agents as simulation results

# EOF