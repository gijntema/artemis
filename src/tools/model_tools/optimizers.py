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
        instructions = {
            "random": self.__make_choice_random,
            "full_heatmap": self.__make_choice_full_heatmap,
            "explore_heatmap": self.__make_choice_explore_heatmap
        }

        return instructions

    def __init_relevant_data(self, choice_method, agent):
        """set up a dictionary containing the relevant functions to extract the data from ForagerAgent need for a specific operations"""
        relevant_data = {}
        return relevant_data

    def __make_choice_random(self):
        chosen = choice(self.choice_indices)
        return chosen

    def __make_choice_full_heatmap(self):
        heatmap = self.relevant_agent_data['heatmap']
        optimal_catch = 0
        optimal_alternative = 'choice_none'
        for alternative in heatmap:
            # discern the catch you would gain according to the information/memory an agent has
            expected_catch = heatmap[alternative]
            if expected_catch > optimal_catch:
                optimal_catch = expected_catch
                optimal_alternative = alternative
        return optimal_alternative

    def __make_choice_explore_heatmap(self):
        pass

    def make_choice(self):
        """method that chooses the data based on the choice method provided"""
        chosen = self.choice_instruction[self.choice_method]()
        return chosen


