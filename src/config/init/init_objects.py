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
This Module contains all functionality to set up the objects needed in further simulations. Specifically, these include
the agents and the choice sets at the core of the model.

Module inputs:
-   the AgentSet and ForagerAgent objects (from agents.py),
-   the ChoiceSet and DiscreteAlternative objects (choice_set.py)
-   the parameters as defined/loaded in init_param.py

Module Usage:
-   this module is used by ARTEMIS.py as the main module needed for initialization of the model

Last Updated:
    06-09-2021

Version Number:
    0.1
"""


from src.tools.model_tools.agents import AgentSet, ForagerAgent
from src.tools.model_tools.choice_set import ChoiceSet, DiscreteAlternative


class ObjectInitializer:
    """class to initialize all objects for the model, specifically
    the ForagerAgents objects (as contained in the AgentSet object) and the
    DiscreteAlternatives (choice options - as contained in the ChoiceSet objects)"""

    def __init__(self):
        """Placeholder in case ObjectInitilializer needs attributes in a later version of the model"""
        pass

    def initialize_choice_set(self, nb_alternatives, init_stock, sd_init_stock, growth_factor=1):
        """" Method to initialise all choice options and trackers related to choice options as contained
        in a ChoiceSet object, with an attribute self.discrete_alternatives referring to a dictionary containing
        all separate choice options and their states/attributes"""
        choice_set = ChoiceSet()
        alternative_tracker = 0
        while alternative_tracker < nb_alternatives:                                                                    # loop the creation of a alternative for the full size of the considered set of choices possibel
            alternative_id = "alternative_" + str(alternative_tracker).zfill(len(str(nb_alternatives)))                 # assign ID
            choice_set.discrete_alternatives[alternative_id] = DiscreteAlternative(alternative_id, init_stock,
                                                                                   sd_init_stock, growth_factor)        # define a single choice option with an ID, initial stock (with an sd) and growth factor
            choice_set.effort_map[alternative_id] = 0                                                                   # define a tracker with 0 effort on each choice option
            choice_set.catch_map[alternative_id] = 0                                                                    # define a tracker with 0 catch on every effort

            alternative_tracker += 1                                                                                    # proceed to next choice_option


        return choice_set

    def initialize_forager_agents(self, nb_agents, choice_set,
                                  catchability_coefficient, nb_alternatives_known,
                                  explore_probability, duration_model,
                                  choice_method="random"):
        """Method to set up the agents in the model"""

        # initialize all agents and time independent tracker variables
        print(choice_method)
        agent_set = AgentSet()                                                                                          # create an instance of the object agent set to contain trackers and agents in
        agent_tracker = 0                                                                                               # make counter for following while loop functioning

        while agent_tracker < nb_agents:
            agent_id = 'agent_' + str(agent_tracker).zfill(len(str(nb_agents)))                                         # construct agent ID
            agent_set.agents[agent_id] = ForagerAgent(choice_set=choice_set,
                                                      choice_method=choice_method,
                                                      agent_id=agent_id,
                                                      catchability_coefficient=catchability_coefficient,
                                                      nb_of_alternatives_known=nb_alternatives_known,
                                                      explore_probability=explore_probability)                          # initialise a ForagerAgent and set up the necessary functioning of attribute ChoiceMaker

            agent_tracker += 1                                                                                          # proceed to next agent

        # initialize all time dependent tracker variables
        # TODO: much of the functioning here can be simplified using collections.defaultdict() objects
        duration_counter = 0                                                                                            # make counter for all time_steps in the model for While loop functioning
        while duration_counter < duration_model:                                                                        # loop over all time steps in the model
            time_id = str(duration_counter).zfill(len(str(duration_model)))
            agent_set.total_time_step_catch_tracker[time_id] = 0                                                        # make entry in time_step specific catch tracker for the specified time step

            agent_tracker = 0                                                                                           # make counter for all time_steps in the model for While loop functioning
            while agent_tracker < nb_agents:                                                                            # loop over all agents
                agent_id = 'agent_' + str(agent_tracker).zfill(len(str(nb_agents)))                                     # set ID of the agent to be modified
                agent_set.agents[agent_id].time_step_catch[time_id] = 0                                                 # for the considered agent, initialise the catch in the given time_step as 0
                agent_tracker += 1                                                                                      # proceed to next agent

            duration_counter += 1                                                                                       # proceed to next time_step

        return agent_set
