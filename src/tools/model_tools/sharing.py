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

-   The HeatmapExchanger class defined here is intended as attribute of ForagerAgent objects,
    as contained in AgentSet objects from agents.py, specifically the heatmap attributes from these objects is given.
    Depending on the sharing strategies also other attributes, like group allegiance are given a reference
    in the HeatmapExchanger class

Module Usage:
-   the module will be used in agents.py to transfer heatmap data from one agent to another

Last Updated:
    18-10-2021

Version Number:
    0.1
"""
import random


# TODO: UNIMPLEMENTED CODE
class HeatmapExchanger:

    def __init__(self, agent,
                 sharing_strategy='random_sharing', receiving_strategy='stubborn_receiver',
                 pick_receiver_strategy='random_choice',
                 number_of_shared_alternatives=1, number_of_agents_shared_with=1):

        self.sharing_strategy = sharing_strategy
        self.pick_receiver_strategy = pick_receiver_strategy
        self.receiving_strategy = receiving_strategy
        self.functionality = self.__init_functionality()
        self.relevant_data = {}                                                                                         # initialise empty data for functionality
        self.relevant_data = self.__init_relevant_data(agent,                                                           # fill relevant data with the data accessed from other objects
                                                       number_of_shared_alternatives,
                                                       number_of_agents_shared_with,
                                                       other_agent_indices=tuple())

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
                        # INSERT FURTHER SHARING FUNCTIONALITY HERE
                    },
                "pick_receiver":
                    {
                        "random_choice":
                            {
                                "init": self.__init_other_agents_random_pick,
                                "execute": self.__pick_receiver_random
                            },
                        "static_group_choice":
                            {
                                'init': self.__init_other_agents_static_group_choice,
                                'execute': self.__pick_receiver_random
                            }
                        # INSERT FURTHER RECEIVER PICKING FUNCTIONALITY HERE
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
                            }                                                                                           # information receiving from other agents is accepted as truth when more recent than own entries, otherwise disregarded -- UNIMPLEMENTED
                        # INSERT FURTHER RECEIVING FUNCTIONALITY HERE
                    }
            }

        return functionality

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------- Initialisation of Strategy Specific Sharing Functionality --------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __init_relevant_data(self, agent, number_of_shared_alternatives, number_of_agents_shared_with, other_agent_indices):
        """returns references to all data/attributes from other objects needed to share or receive data"""
        self.relevant_data['agent_id'] = agent.id
        sharing_relevant = self.functionality['sharing'][self.sharing_strategy]['init'](agent)                          # generate references to the relevant data for the specified sharing strategy
        receiving_relevant = self.functionality['receiving'][self.receiving_strategy]['init'](agent)                    # generate references to the relevant data for the specified sharing strategy

        external_relevant = self.__init_relevant_external_parameters(number_of_shared_alternatives,                     # generate a dictionary with the relevant parameters defined
                                                                     number_of_agents_shared_with,)

        functionality_relevant_data = sharing_relevant | receiving_relevant                                             # combine relevant data for sharing and receiving into one data object
        relevant_data = functionality_relevant_data | external_relevant                                                 # add the defined parameters for sharing to the relevant data

        return relevant_data

    def __init_relevant_no_sharing(self, agent):
        relevant_data = dict()
        relevant_data['agent_id'] = agent.id
        return relevant_data

    def __init_relevant_random_sharing(self, agent):
        relevant_data = dict()
        relevant_data['agent_id'] = agent.id
        relevant_data['heatmap'] = agent.heatmap
        relevant_data['known_alternatives'] = agent.list_of_known_alternatives
        return relevant_data

    def __init_relevant_group_sharing(self, agent):
        ## TODO: OBSOLETE CODE, IMPLEMENTED IN PICK RECEIVER STRATEGIES BELOW
        relevant_data = dict()
        relevant_data['agent_id'] = agent.id
        relevant_data['heatmap'] = agent.heatmap
        relevant_data['group_allegiance'] = "NOT IMPLEMENTED"
        relevant_data['known_alternatives'] = agent.list_of_knowns_alternatives
        return relevant_data

    def __init_relevant_external_parameters(self, number_of_alternatives_shared=1, number_of_agents_shared_with=1):
        relevant_data = dict()
        relevant_data['number_of_shared_alternatives'] = number_of_alternatives_shared                                  # load number of choice options that need to be shared with other agents
        relevant_data['number_of_agents_shared_with'] = number_of_agents_shared_with                                    # load the number of agents the choice options are shared
        return relevant_data
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------- Initialisation of Strategy Pick Receiver Functionality ---------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __init_other_agents_random_pick(self, agent_set):
        """Methods for initiliazing a list of agents to pick from"""
        list_of_agents = list(agent_set.agents.keys())                                                                  # agents to pick as receiver include all agents
        self.relevant_data['other_agent_indices'] = \
            [x for x in list_of_agents if x is not self.relevant_data['agent_id']]                                      # exclude agent itself as potential receiver and load result into relevant data

    def __init_other_agents_static_group_choice(self, agent_set):
        input_data = agent_set.group_former.relevant_data                                                               # access the data in contained in the GroupFormer object
        personal_id = self.relevant_data['agent_id']                                                                    # access personal id
        personal_allegiance = input_data['personal_allegiances'][personal_id]                                           # identify which group the agent belongs to
        group_memberships = input_data['overview_allegiances']                                                          # access data with what agents belong to what groups
        list_of_agents = group_memberships[personal_allegiance]                                                         # identify what agents belong to the group the agent belongs to

        self.relevant_data['other_agent_indices'] = \
            [x for x in list_of_agents if x is not self.relevant_data['agent_id']]                                      # exclude agent itself as potential receiver and load result into relevant data
        self.relevant_data['group_allegiance'] = personal_allegiance

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
# ---------------------------------------  Main Method to Provide Heatmap Data ----------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def provide_data(self, agent_set):
        share_partner_counter = 0                                                                                       # initialise counter to loop over the agents data will be shared to
        while share_partner_counter < self.relevant_data['number_of_agents_shared_with']:                               # loop over all agents that are picked to receive data

            print('<{}> Choosing receiver according to <{}>'.format(self.relevant_data['agent_id'],
                                                                    self.pick_receiver_strategy))
            picked_receiver = self.functionality['pick_receiver'][self.pick_receiver_strategy]['execute']()             # pick the agent that will receive information
            print('<{}> Sharing data according to <{}>'.format(self.relevant_data['agent_id'],
                                                               self.sharing_strategy))
            shared_data = self.functionality['sharing'][self.sharing_strategy]['execute']()                             # pick data to be given to the considered receiver agent

            receiver_agent = agent_set.agents[picked_receiver].heatmap_exchanger                                        # shorten the reference to the receiver agents Heatmap exchanger tool for visual aid in the script
            print('<{}> Receiving data according to <{}>'.format(receiver_agent.relevant_data['agent_id'],
                                                                 receiver_agent.receiving_strategy))
            receiver_agent.functionality['receiving'][receiver_agent.receiving_strategy]['execute'](shared_data)        # make the receiver agent accept/reject the given data based on their receiving strategy

            self.__save_received_timestamp(shared_data)                                                                 # TODO: CHECK WHAT I WANTED TO DO HERE
            share_partner_counter += 1                                                                                  # proceed to pick next receiver agent and the data to be shared with that agent (if more than 1 share agent)
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------  Strategy Choice for Data Sharing -------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __share_no_sharing(self):
        """method that does not share any data"""
        shared_alternatives = tuple()
        return shared_alternatives

    def __share_random_sharing(self):
        """method that shares a random x known data points from heatmap"""
        shared_alternatives_indices = []
        shared_alternatives_data = []
        if not isinstance(self.relevant_data['number_of_shared_alternatives'], int) \
                and not isinstance(self.relevant_data['number_of_shared_alternatives'], float)\
                and self.relevant_data['number_of_shared_alternatives'] != 'ALL':
            raise TypeError("number can only be an integer or ALL")

        elif self.relevant_data['number_of_shared_alternatives'] == 'ALL':                                              # share all data
            shared_alternatives_indices = self.relevant_data['known_alternatives']                                      # to be shared indices are all indices memory has an entry on
            for alternative in shared_alternatives_indices:
                shared_alternatives_data.append(self.relevant_data['heatmap'][alternative])

        else:
            # TODO: FIX quick fix of number of shared alternatives > number of known alternatives
            # floor division to split certainly shared and chance at sharing
            certain_shares = self.relevant_data['number_of_shared_alternatives'] // 1                                   # get al wholes as the number of alternatives that will be shared with 100% certainty
            probability_share_additional = self.relevant_data['number_of_shared_alternatives'] % 1                      # get the chance of sharing an additional value (e.g. if number of shared alternatives = 2.5, in 50% chance of the time an agent wil share 2 alternatives and in 50% of the time it will share 3 alternatives)

            # set number of alternatives to be shared, including uncertainties in this number
            number_of_shared_alternatives = certain_shares
            if random.random() < probability_share_additional:                                                          # check if a ranomd number between 0 and 1 is larger than the probability of sharing an extra alternative
                number_of_shared_alternatives += 1                                                                      # share another alternative

            alternative_counter = 0
            while alternative_counter < number_of_shared_alternatives:
                shared_alternative = random.choice(self.relevant_data['known_alternatives'])                            # pick a random choice option index the agents memory has an entry on
                if shared_alternative not in shared_alternatives_indices:                                               # check if we are not already sharing this choice option
                    shared_alternatives_indices.append(shared_alternative)                                              # attach the choice option index from the randomly chosen entry
                    shared_alternatives_data.append(self.relevant_data['heatmap'][shared_alternative])                  # attach the choice option contents from the randomly chosen entry
                alternative_counter += 1

        return tuple((shared_alternatives_indices, shared_alternatives_data))

    def __share_group_sharing(self):
        shared_alternatives = tuple()
        return shared_alternatives

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------  Strategy Choice for picking a receiver ----------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __pick_receiver_random(self):
        receiver_agent = random.choice(self.relevant_data['other_agent_indices'])

        if 'group_allegiance' in self.relevant_data:                                                                    # simple check to find out if the agent is really only sharing within its own group
            print('<{}> with allegiance <{}> has chosen <{}> as receiver of the heatmap sharing'\
                  .format(self.relevant_data['agent_id'],
                          self.relevant_data['group_allegiance'],
                          receiver_agent))

        return receiver_agent

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------  Strategy Specific Receiving --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __receive_no_receiver(self, received_heatmap_data=tuple()):
        """function that does not do anything to signal rejection of shared data"""
        pass

    def __receive_willing_receiver(self, received_heatmap_data=tuple()):
        """function that willingly accepts any data shared as new heatmap entry, overwriting any existing entries"""
        received_alternative_indices = received_heatmap_data[0]
        received_alternative_data = received_heatmap_data[1]

        received_counter = 0
        while received_counter < len(received_alternative_indices):
            # add knowledge if the alternative is unknown
            received_index = received_alternative_indices[received_counter]                                             # get index of a single shared choice option
            received_data = received_alternative_data[received_counter]
            self.relevant_data['heatmap'][received_index] = received_data                                           # fill the empty choice option entry with the received data

            received_counter += 1

    def __receive_combine_receiver(self, received_heatmap_data=tuple()):
        """function that accepts any data shared.
        if any knowledge on the shared data points is already in the heatmap,
        the agent will take the average as new entry.
        If no knowledge is present the provided data is accepted as new heatmap entry"""
        received_alternative_indices = received_heatmap_data[0]
        received_alternative_data = received_heatmap_data[1]

        received_counter = 0
        while received_counter < len(received_alternative_indices):
            # add knowledge if the alternative is unknown
            received_index = received_alternative_indices[received_counter]                                             # get index of a single shared choice option
            received_data = received_alternative_data[received_counter]                                                 # get contents of a single shared choice option

            # add knowledge if the alternative is unknown
            if isinstance(self.relevant_data['heatmap'][received_index], int):                                          # check if the receiving agent already has an entry for that choice: NO
                self.relevant_data['heatmap'][received_index] = received_data                                           # fill the empty choice option entry with the received data

            # When the receiving agent already has knowledge on the shared knowledge, take the average of both
            elif isinstance(self.relevant_data['heatmap'][received_index], float):                                      # check if the receiving agent already has an entry for that choice: YES
                self.relevant_data['heatmap'][received_index] = \
                    (received_data + self.relevant_data['heatmap'][received_index])/2                                   # take average of newly shared data and the information already known from other data

            received_counter += 1

    def __receive_stubborn_receiver(self, received_heatmap_data=tuple()):
        """function that accepts data shared only if the entry is not in the personal heatmap yet."""
        received_alternative_indices = received_heatmap_data[0]
        received_alternative_data = received_heatmap_data[1]

        received_counter = 0
        while received_counter < len(received_alternative_indices):
            # add knowledge if the alternative is unknown
            received_index = received_alternative_indices[received_counter]                                             # get index of a single shared choice option
            received_data = received_alternative_data[received_counter]                                                 # get contents of a single shared choice option

            # add knowledge if the alternative is unknown
            if isinstance(self.relevant_data['heatmap'][received_index], int):                                          # check if the receiving agent already has an entry for that choice: NO
                self.relevant_data['heatmap'][received_index] = received_data

            received_counter += 1

    def __receive_recency_receiver(self, received_heatmap_data=tuple()):
        """function that accepts data as new entry if the data was obtained in a more recent time step
        than the heatmap entry already present"""
        pass  # UNIMPLEMENTED, AGE OF INFORMATION CURRENTLY NOT TRACKED

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------  Ensure Age of Information is saved -----------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __save_received_timestamp(self, shared_data):  # TODO IMPLEMENTED AGE OF MEMORY FUNCTIONALITY
        pass
