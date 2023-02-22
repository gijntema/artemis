#
# This file is part of ARTEMIS (https://git.wur.nl/artemis.git).
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
This Module is aimed at handling and executing how agents are ordered.
"""
import random

class AgentOrderer:

    def __init__(self, agent, strategy):

        self.agent_indices = agent.agent_index_list
        self.strategy = strategy
        self.functionality = self.__init_functionality()

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------- Define General Functionality --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def __init_functionality(self):
        functionality = \
            {
                "shuffle":
                    {
                        "execute": self.__order_shuffle
                    },
                "constant":
                    {
                        "execute": self.__order_none
                    }
            }
        return functionality

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------- Initialisation of Strategy Specific Ordering Functionality -------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def __order_none(self):
        return self.agent_indices

    def __order_shuffle(self):
        ordered_agent_indices = self.agent_indices.copy()
        random.shuffle(ordered_agent_indices)   
        return ordered_agent_indices

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------  Main Method to Order Agents -------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def run_ordering(self):
        return self.functionality[self.strategy]["execute"]()
