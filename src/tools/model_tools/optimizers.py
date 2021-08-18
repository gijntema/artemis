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

# TODO: --STRUCTURAL-- implement functionality so optimizers can be outside of the AgentSet/ForagerAgent class
from collections import defaultdict


class ChoiceMaker:
    def __init__(self, choice_method='default', agent='ForagerAgent Placeholder'):
        self.instruction_dictionary = self.__init_functionality
        self.choice_method = choice_method
        self.relevant_data = self.__dict_relevant_data(agent)

    def __init_functionality(self):
        instructions = defaultdict(int)
        return instructions

    def __dict_relevant_data(self, choice_method, agent):
        """set up a dictiornary containing the relevant functions to extract the data from ForagerAgent need for a specific operaions"""
        relevant_data = defaultdict(int)
        if relevant_data[choice_method] == int():
            raise NotImplementedError('Choice made based on the method {} is not supported'.format(choice_method))
        else:
            "smurf"
        return relevant_data

    def make_choice(self, agent):
        """method that chooses the data based on the choice method provided"""
        # 1) read dictionary entry for Choice_method giving instructions to:
        # 2) make choice




