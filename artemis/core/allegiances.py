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
from random import shuffle
from copy import deepcopy
"""
This Module is used to handle group formation in agent sharing mechanisms and the class GroupFormer()
is meant as attribute of the AgentSet object in agents.py

Module inputs:
-   parameters from init_param.py

Module Usage:
-   As attribute of the AgentSet() object in agents.py

Last Updated:
    22-10-2021

Version Number:
    0.1
"""

# TODO UNIMPLEMENTED FUNCTIONALITY
class GroupFormer:

    def __init__(self, agent_set, number_of_groups=None,
                 division_style='equal_mutually_exclusive_groups',
                 group_dynamics=False):

        self.functionality = self.__init_functionality()
        self.dynamics = group_dynamics
        self.relevant_data = self.__init_relevant_data(number_of_groups, division_style, agent_set)


    def __init_functionality(self):
        functionality = \
            {
                'init':
                    {
                        'equal_mutually_exclusive_groups': self.__init_equal_mutually_exclusive_groups,
                        'unequal_groups': "PLACEHOLDER FOR UNEQUAL GROUP DISTRIBUTION"

                    },
                'dynamics':
                    {
                        'PLACEHOLDER': 'PLACEHOLDER'
                    }

                # ENTER FUTURE FUNCTIONALITY HERE
            }

        return functionality

    def __init_relevant_data(self, number_of_groups, division_style, agent_set):
        relevant_data = dict()
        relevant_data['overview_allegiances'], relevant_data['personal_allegiances'] =\
            self.__init_allegiances(number_of_groups, division_style, agent_set)
        return relevant_data

    def __init_allegiances(self, number_of_groups, division_style, agent_set):
        allegiances = self.functionality['init'][division_style](number_of_groups, agent_set)
        return allegiances

    def __init_equal_mutually_exclusive_groups(self, number_of_groups, agent_set):
        overview_allegiances = {}
        personal_allegiances = {}
        agent_list = list(agent_set.agents.keys())
        shuffle(agent_list)                                                                                             # Shuffle agents list for random assigning of allegiances

        agent_group_size = int(len(agent_set.agents)/number_of_groups)                                                  # quick and dirty way to assign groups
        agent_start_index = 0
        agent_end_index = agent_group_size

        group_counter = 0
        while group_counter < number_of_groups:

            overview_allegiances['group_{}'.format(group_counter)] = \
                deepcopy(agent_list[agent_start_index:agent_end_index])

            agent_start_index += agent_group_size
            agent_end_index += agent_group_size
            group_counter += 1

        for group in overview_allegiances:
            for agent in overview_allegiances[group]:
                personal_allegiances[agent] = group

        return overview_allegiances, personal_allegiances
