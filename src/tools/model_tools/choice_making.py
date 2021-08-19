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

# TODO: --STRUCTURAL-- implement functionality so optimizers can be outside of the AgentSet/ForagerAgent class
from random import choice, random


class ChoiceMaker:
    def __init__(self, choice_set, choice_method='random', agent='ForagerAgent Placeholder'):
        self.choice_indices = list(choice_set.discrete_alternatives.keys())
        self.choice_instruction = self.__init_instructions()
        self.choice_method = choice_method
        self.relevant_agent_data = self.__init_relevant_data(agent)

    def __init_instructions(self):
        # all entries are REFERENCES to function object, which are only executed when () are added (see line 76)
        instructions = {

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
        """set up a dictionary containing the relevant functions to extract the data from ForagerAgent need for a specific operations"""

        relevant_data = self.choice_instruction[self.choice_method]['init'](agent)
        return relevant_data

    def __init_relevant_random(self, agent):
        return dict()

    def __init_relevant_full_heatmap(self, agent):
        relevant_data = dict()
        relevant_data['heatmap'] = agent.heatmap
        return relevant_data

    def __init_relevant_explore_heatmap(self, agent):
        relevant_data = dict()
        relevant_data['explore_probability'] = agent.explore_probability
        relevant_data['heatmap'] = agent.heatmap
        return relevant_data
# ----------------------------------------------------------------------------------------------------------------------
# Methods that make the actual for the ForagerAgent
# ----------------------------------------------------------------------------------------------------------------------

    def __make_choice_random(self):
        chosen = choice(self.choice_indices)
        return chosen

    def __make_choice_full_heatmap(self):
        heatmap = self.relevant_agent_data['heatmap']
        optimal_catch = 0
        chosen = 'choice_none'
        for potential_choice in heatmap:
            # discern the catch you would gain according to the information/memory an agent has
            expected_catch = heatmap[potential_choice]
            if expected_catch > optimal_catch:
                optimal_catch = expected_catch
                chosen = potential_choice

        return chosen

    def __make_choice_explore_heatmap(self):
        if random < self.relevant_agent_data['explore_probability']:
            chosen = self.__make_choice_random()
        else:
            chosen = self.__make_choice_full_heatmap()

        return chosen

    def make_choice(self):
        """method that chooses the data based on the choice method provided"""
        chosen = self.choice_instruction[self.choice_method]['choose']()
        return chosen


