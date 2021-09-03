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
This Module is used to determine the way any ForagerAgent might choose any of the given choice options
(e.g. what cell to fish in, what patch of bush to forage on, what resource search tactic to use,
what mode of transportation to use etc.).

All functionality is contained in methods and attributes of the ChoiceMaker object, The ChoiceMaker object is key for
any ForagerAgent object to choose a forage option

Module inputs:
-   loads parts of an ForagerAgent Object during the init (PLEASE ALWAYS AVOID CIRCULAR REFERENCES, see module usage)

Module Usage:
-   Used by the module agents.py as part of the ForagerAgent object

Last Updated:
    03-09-2021

Version Number:
    0.1
"""

from random import choice, random


class ChoiceMaker:
    def __init__(self, choice_set, choice_method='random', agent='ForagerAgent Placeholder'):                           # initilisation statement
        self.choice_indices = list(choice_set.discrete_alternatives.keys())                                             # initialise list of potential choice options the agent can choose from
        self.choice_instruction = self.__init_instructions()                                                            # initialise dictionary with all references to all potential functionality of a ChoiceMaker object
        self.choice_method = choice_method                                                                              # indication of the functionality this specific instance of ChoiceMaker should have
        self.relevant_agent_data = self.__init_relevant_data(agent)                                                     # using self.choice method, acquire references to the specific parts of an agent that this specific instance of ChoiceMaker should have access to

# ----------------------------------------------------------------------------------------------------------------------
# Methods that initialise the functionality of the ChoiceMaker
# ----------------------------------------------------------------------------------------------------------------------

    def __init_instructions(self):
        """define a dictionary containing entries for all supported choice making methods, providing instructions
        on the initialization of the ChoiceMaker Object and how to make a choice from provided options for foraging,
        based on a 'choice_method' name as indication of the way to choose options"""

        instructions = {
            # all entries are REFERENCES to method object, which are only executed when () are added (see line 82)

            "random": {
                'init': self.__init_relevant_random,
                'choose': self.__make_choice_random
            },

            "full_heatmap": {
                'init': self.__init_relevant_full_heatmap,
                'choose': self.__make_choice_full_heatmap
            },

            "explore_heatmap": {
                'init': self.__init_relevant_explore_heatmap,
                'choose': self.__make_choice_explore_heatmap
            }

            # include further decision making options HERE (and as methods below)
        }

        return instructions

    def __init_relevant_data(self, agent):
        """set up a dictionary containing the relevant functions to extract the data from ForagerAgent
        needed for this specific instance of ChoiceMaker"""

        relevant_data = self.choice_instruction[self.choice_method]['init'](agent)
        return relevant_data

    def __init_relevant_random(self, agent):
        """" initialises the data needed for the 'random' choice method: a reference to:
        - No data needed, so an empty dictionary"""
        return dict()

    def __init_relevant_full_heatmap(self, agent):
        """" initialises the data needed for the 'full_heatmap' choice method: a reference to:
        - the agent heatmap"""
        relevant_data = dict()
        relevant_data['heatmap'] = agent.heatmap                                                                        # load agent heatmap
        return relevant_data

    def __init_relevant_explore_heatmap(self, agent):
        """" initialises the data needed for the 'explore_heatmap' choice method: a reference to:
        - the agent heatmap and
        - the agent explore probability"""
        relevant_data = dict()                                                                                          # initialise data dictionary
        relevant_data['explore_probability'] = agent.explore_probability                                                # load explore probability
        relevant_data['heatmap'] = agent.heatmap                                                                        # load agent heatmap
        return relevant_data

# ----------------------------------------------------------------------------------------------------------------------
# Methods that make the actual choice for the ForagerAgent
# ----------------------------------------------------------------------------------------------------------------------

    def __make_choice_random(self):
        """method to choose a random choice option to forage in"""
        chosen = choice(self.choice_indices)
        return chosen

    def __make_choice_full_heatmap(self):
        """method to choose an option based on the maximum catch according to an agent heatmap
        returns the dictionary key of that maximum"""
        heatmap = self.relevant_agent_data['heatmap']
        chosen = max(heatmap, key=heatmap.get)                                                                          # returns key of the maximum value
        return chosen

    def __make_choice_explore_heatmap(self):
        """method to choose an option based on either the full_heatmap or random methods,
        according to a fixed probability"""
        if random < self.relevant_agent_data['explore_probability']:                                                    # if a random number between 0 and 1 is smaller than the explore probability, the ForagerAgent will explore a random cell
            chosen = self.__make_choice_random()
        else:                                                                                                           # if a random number between 0 and 1 is larger than the explore probability, the ForagerAgent will choose based on the heatmap
            chosen = self.__make_choice_full_heatmap()

        return chosen

    def make_choice(self):
        """method that chooses the data based on the choice method provided
        as key for the internal instructions dictionary"""
        chosen = self.choice_instruction[self.choice_method]['choose']()
        return chosen


