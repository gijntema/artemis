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
This Module is aimed at handling and executing how agents share data contained in their heatmaps

this module is read by run_model.py to be used to provide information to other agents
and how to receive data from other agents

Module inputs:

-   The HeatmapSharer class defined here is intended as attribute of ForagerAgent objects,
    as contained in AgentSet objects from agents.py, specifically the heatmap attributes from these objects is given.
    Depending on the sharing strategy also other attributes, like group allegiance are given a reference
    in the HeatmapSharer class

Module Usage:
-   the module will be used in agents.py to transfer heatmap data from one agent to another

Last Updated:
    07-10-2021

Version Number:
    0.1
"""

# TODO: UNFINISHED, UNFUNCTIONAL CODE
class HeatmapSharer:

    def __init__(self, agent, other_agent_indices=tuple(),
                 sharing_strategy='random_sharing', receiving_strategy='combiner_receiver',
                 number_of_shared_alternatives=1, number_of_agents_shared_with=1):

        self.sharing_strategy = sharing_strategy
        self.receiving_strategy = receiving_strategy
        self.functionality = self.__init_functionality()
        self.relevant_data = self.__init_relevant_data(agent,
                                                       number_of_shared_alternatives,
                                                       number_of_agents_shared_with)

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------- Define General Functionality --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def __init_functionality(self):
        functionality = \
            {
                "sharing":
                    {
                        "no_sharing":                                                                                   # information sharing turned off, agent does not provide other with any information it has collected
                            {
                                "init": self.__init_relevant_no_sharing,
                                "execute": self.__share_no_sharing
                            },
                        "random_sharing":
                            {
                                "init": self.__init_relevant_random_sharing,
                                "execute": self.__share_random_sharing
                            },                                                                                          # information sharing in x random options to y random people
                        "group_sharing":
                            {
                                "init": self.__init_relevant_group_sharing,
                                "execute": self.__share_group_sharing
                            }                                                                                           # information sharing as x random options to y random people that an agent shares group allegiance with
                    },
                "receiving":
                    {
                        "no_receiver":
                            {
                                "init": self.__init_relevant_no_receiver,
                                "execute": self.__receive_no_receiver
                            },                                                                                          # information receiving absent, as agent does not accept data from anyone else
                        "willing_receiver":
                            {
                                "init": self.__init_relevant_willing_receiver,
                                "execute": self.__receive_willing_receiver
                            },                                                                                          # information receiving from other agents is always accepted as truth (overwrite entry)
                        "combine_receiver":
                            {
                                "init": self.__init_relevant_combine_receiver,
                                "execute": self.__receive_combine_receiver
                            },                                                                                          # information receiving from other agents is accepted as truth (overwrite entry) when no knowledge on option is present at oneself, otherwise taken as the mean of both
                        "stubborn_receiver":
                            {
                                "init": self.__init_relevant_stubborn_receiver,
                                "execute": self.__receive_stubborn_receiver
                            },                                                                                          # information receiving from other agents is accepted as truth (overwrite entry) when no knowledge on option is present at oneself, otherwise disregarded
                        "recency_receiver":
                            {
                                "init": self.__init_relevant_recency_receiver,
                                "execute": self.__receive_recency_receiver
                            }                                                                                           # information receiving from other agents is accepted as truth when more recent than own entries, otherwise disregarded
                    }
            }

        return functionality

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------- Initialisation of Strategy Specific Sharing Functionality --------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __init_relevant_data(self, agent, number_of_shared_alternatives, number_of_agents_shared_with):
        """returns references to all data/attributes from other objects needed to share or receive data"""
        sharing_relevant = self.functionality['sharing'][self.sharing_strategy]['init'](agent)                          # generate references to the relevant data for the specified sharing strategy
        receiving_relevant = self.functionality['receiving'][self.receiving_strategy]['init'](agent)                    # generate references to the relevant data for the specified sharing strategy

        external_relevant = self.__init_relevant_external_parameters(number_of_shared_alternatives,                     # generate a dictionary with the relevant parameters defined
                                                                     number_of_agents_shared_with)

        functionality_relevant_data = sharing_relevant | receiving_relevant                                             # combine relevant data for sharing and receiving into one data object
        relevant_data = functionality_relevant_data | external_relevant                                                 # add the defined parameters for sharing to the relevant data

        return relevant_data

    def __init_relevant_no_sharing(self, agent):
        relevant_data = dict()
        return relevant_data

    def __init_relevant_random_sharing(self, agent):
        relevant_data = dict()
        relevant_data['heatmap'] = agent.heatmap
        return relevant_data

    def __init_relevant_group_sharing(self, agent):
        relevant_data = dict()
        relevant_data['heatmap'] = agent.heatmap
        relevant_data['group_allegiance'] = "NOT IMPLEMENTED"
        return relevant_data

    def __init_relevant_external_parameters(self, number_of_alternatives_shared=1, number_of_agents_shared_with=1):
        relevant_data = dict()
        relevant_data['number_of_shared_alternatives'] = number_of_alternatives_shared                                  # load number of choice options that need to be shared with other agents
        relevant_data['number_of_agents_shared_with'] = number_of_agents_shared_with                                    # load the number of agents the choice options are shared
        return relevant_data

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------- Initialisation of Strategy Specific Receiving Functionality -------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __init_relevant_no_receiver(self, agent):
        relevant_data = dict()
        return relevant_data

    def __init_relevant_willing_receiver(self, agent):
        relevant_data = dict()
        relevant_data['heatmap'] = agent.heatmap
        return relevant_data

    def __init_relevant_combine_receiver(self, agent):
        relevant_data = dict()
        relevant_data['heatmap'] = agent.heatmap
        return relevant_data

    def __init_relevant_stubborn_receiver(self, agent):
        relevant_data = dict()
        relevant_data['heatmap'] = agent.heatmap
        return relevant_data

    def __init_relevant_recency_receiver(self, agent):
        relevant_data = dict()
        relevant_data['heatmap'] = agent.heatmap
        return relevant_data

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------  Main Method to Share Data ---------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def share_data(self):
        shared_data = self.functionality['sharing'][self.sharing_strategy]['execute']()
        self.functionality['receiving'][self.receiving_strategy]['execute'](shared_data)
        self.__save_received_timestamp(shared_data)

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------  Strategy Specific Sharing ---------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __share_no_sharing(self):
        shared_alternatives = tuple()
        return shared_alternatives

    def __share_random_sharing(self):
        share_partner_counter = 0                                                                           # initialise counter to loop over the agents data will be shared to
        while share_partner_counter < self.relevant_data['number_of_agents_shared_with']:                                                       # loop over all agents that are picked to receive data
            shared_heatmap_data = agent_set.agents[agent].share_heatmap_knowledge(                          # identify what data will be shared with another agent
                number_of_alternatives=shared_alternatives)
            data_receiver_agent = random.choice(agent_index_list)                                           # pick random agent to share with
            agent_set.agents[data_receiver_agent].receive_heatmap_knowledge(shared_heatmap_data, time_id)   # picked agent receives data
            print('{} is now sharing data on stock(s) in {} with {}'.format(str(agent),                     # report on data sharing
                                                                            str(shared_heatmap_data[0]),
                                                                            str(data_receiver_agent)))
            share_partner_counter += 1

    shared_alternatives = tuple()
        return shared_alternatives

    def __share_group_sharing(self):
        shared_alternatives = tuple()
        return shared_alternatives

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------  Strategy Specific Receiving --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __receive_no_receiver(self, received_alternatives=tuple()):
        pass

    def __receive_willing_receiver(self, received_alternatives=tuple()):
        self.relevant_data

    def __receive_combine_receiver(self, received_alternatives=tuple()):
        self.relevant_data

    def __receive_stubborn_receiver(self, received_alternatives=tuple()):
        self.relevant_data

    def __receive_recency_receiver(self, received_alternatives=tuple()):
        self.relevant_data
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------  Ensure Age of Information is saved -----------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __save_received_timestamp(self, shared_data):  # TODO IMPLEMENTED AGE OF MEMORY FUNCTIONALITY
        pass



