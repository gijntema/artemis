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
This Module is used to define the individual agents used in the model (ForagerAgent object and it's derivatives
FishermanAgent and PredatorAgent) as well as the overarching object AgentSet, containing all ForagerAgent objects
and overarching trackers/functionality

All agent specific functionality and tracking is contained in methods and attributes of the ForagerAgent
(and it's derivatives FishermanAgent and PredatorAgent). Additionally tracking and more general operations concerning
all agents are in the AgentSet object

Module inputs:
-   ChoiceMaker object from choice_making.py as an attribute of ForagerAgents (and it's derivatives)
-   the ChoiceSet object (and its content, including the DiscreteAlternative object) to have a memory of the options for
    making choices regarding foraging

Module Usage:
-   init_objects.py uses the module to initialize all objects needed at any later stage in the model
-   run_model.py uses the module to execute agent operations
-   choice_making.py loads parts of the ForagerAgent object as input for the ChoiceMaker object

Last Updated:
    06-09-2021

Version Number:
    0.1
"""



import random
from collections import defaultdict  # TODO: --STRUCTURAL-- Replace difficult initialisation
from src.tools.model_tools.choice_making import ChoiceMaker


# TODO: --MINOR-- hide internal functions

class AgentSet:                                         # to be implemented, not yet included in the other scripts
    """Class to contain both the agents in ForagerAgent objects (or a more specified version of it)
    and global data on all agents in the model """
    def __init__(self):
        self.agents = {}                                # dictionary with all agents as ForagerAgent objects
        self.total_catch = 0                            # Tracker for total catch of all agents and time_steps combined
        self.total_time_step_catch_tracker = {}         # tracker for total catch each time_step
        self.average_time_step_catch_tracker = {}       # tracker for average catch each time_step
        self.time_step_catch_distribution = {}          # tracker to save distribution of catch over the agents for every time_step

    def update_agent_trackers(self, agent_id, catch, alternative_index, time_tracker):
        """" updates the data contained in a single ForagerAgent
        as well as the more general agent trackers in AgentSet"""

        self.agents[agent_id].update_agent_trackers(alternative_index=alternative_index, catch=catch,                   # update single agent trackers
                                                   time_step_counter=time_tracker)

        self.__update_total_catch(catch)                                                                                # update overall catch
        self.__update_total_time_step_catch(catch, time_tracker)                                                        # updates the catch per time_step

    def __update_total_catch(self, catch):
        """updates the total catch by the given amount from a single catch event"""
        self.total_catch += catch

    def __update_average_time_step_catch(self):
        """" average tracker not yet implemented
        -- could represent the average catch of all agents in a given time_step  in future functionality--"""
        pass

    def __update_total_time_step_catch(self, catch, time_tracker):
        """updates the total catch in a given time step by the given amount from a single catch event"""
        self.total_time_step_catch_tracker[str(time_tracker)] += catch


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- the ForagerAgent object -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class ForagerAgent:
    """general class to define objects as agents that may forage from a resource and their attributes"""
    def __init__(self, choice_set, choice_method):
        self.forage_catch_tracker = {}                                                                                  # tracker variable for total catch gained from each alternative
        self.forage_effort_tracker = {}                                                                                 # tracker variable for effort exerted on each alternative
        self.heatmap = {}                                                                                               # agents memory on the last forage event in each alternative
        self.total_catch = 0                                                                                            # tracker variable to track total catch for this agent
        self.catchability_coefficient = 0                                                                               # efficiency of resource uptake of the agent
        self.explore_probability = 0                                                                                    # chance an agent chooses a random alternative (when allowed)
        self.id = "no_id"                                                                                               # id consistent with other indices used in the rest of the model
        self.time_step_catch = {}                                                                                       # tracker variable to check time_step fluctuations in catch
        self.list_of_known_alternatives = []                                                                            # list of alternatives that an agent has information on

        self.choice_maker = ChoiceMaker(choice_set=choice_set,                                                          # object that identifies/loads the relevant data from ForagerAgents and can make foraging decisions for ForagerAgents based on that data
                                        choice_method=choice_method,
                                        agent=self)
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------Method to initialize agents before running the main model --------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    # TODO: STRUCTURAL: currently initialization method is called in the ObjectInitializer (init_objects.py)
    #  however this should be migrated to ForagerAgent.__init__() since this in explicitly meant for this purpose

    def initialize_content(self,
                           choice_set,
                           agent_id,
                           catchability_coefficient,
                           nb_of_alternatives_known,
                           explore_probability):
        """"Method to initialize the ForagerAgent based on input data"""

        # initialise all maps containing data on expectations and results of forage events
        choice_set_length = len(choice_set.discrete_alternatives)                                                       # identify number of choice options
        alternative_indices = self.__initialize_choice_set_mirrors(choice_set_length)                                   # generate list of all choice option indices

        # fill heatmap with initial known alternatives
        list_of_knowns = self.__initialize_list_of_knowns(nb_of_alternatives_known, alternative_indices)                # choose a random nb_of_alternatives_known number as initial data a ForagerAgent has memory on at the start of a simulation
        # add the heatmap data for each cell initially known as the catch they would get when fishing there at t=0
        self.__initialize_fill_heatmap(list_of_knowns, choice_set, catchability_coefficient)                            # read the choice set to acquire stock values for the choice options a ForagerAgent knows and enter these in the ForagerAgent memory (self.heatmap)

        # include final internal measures of the agent
        self.id = agent_id                                                                                              # set agent id
        self.catchability_coefficient = catchability_coefficient                                                        # set catchability coefficient
        self.explore_probability = explore_probability                                                                  # set chance to explore a random cell if the scenario allows this
        self.list_of_known_alternatives = list_of_knowns                                                                # attach list of indices with choice options the ForagerAgent has a memory on at the start of the model - INDICES can be duplicates and Agents may therefore not know nb_of alternatives_known at the start

    def __initialize_choice_set_mirrors(self, choice_set_length):
        """build a list of choice option indices to serve as a basis
        to initialise the ForagerAgent memory and data trackers with"""
        alternative_indices = []
        alternative_tracker = 0
        while alternative_tracker < choice_set_length:
            alternative_id = "alternative_" + str(alternative_tracker).zfill(len(str(choice_set_length)))               # add 0s before the index number until it has a length of four digits
            self.forage_catch_tracker[alternative_id] = 0                                                               # load index in map with previous yield per alternative
            self.forage_effort_tracker[alternative_id] = 0                                                              # load index in map with previous effort per alternative
            self.heatmap[alternative_id] = 0                                                                            # load index in map with expectations per alternative
            alternative_indices.append(alternative_id)                                                                  # construct list of indeces list for later (external) use
            alternative_tracker += 1                                                                                    # proceed to the next alternative

        return alternative_indices                                                                                      # return list of all choice options in the model

    def __initialize_list_of_knowns(self, nb_of_alternatives_known, alternative_indices):
        """initialises a list of #(nb_of_alternatives_known) choice option indices to
        simulate what choice options have already been foraged in before the start of a simulation"""
        list_of_knowns = []
        i = 0                                                                                                           # counter to track loop with
        while i < nb_of_alternatives_known:                                                                             # loop to generate all knowns choice options
            # choose a random alternatives that the agent will know
            list_of_knowns.append(random.choice(alternative_indices))                                                   # choose a random
            i += 1                                                                                                      # proceed to generate the next known choice option

        return list_of_knowns                                                                                           # return list of initial known choice options of an Agent

    def __initialize_fill_heatmap(self, list_of_knowns, choice_set, catchability_coefficient):
        """use the list of known choice options to fill the expected catches in the memory of the agent"""
        for known_cell in list_of_knowns:
            self.heatmap[known_cell] = \
                choice_set.discrete_alternatives[known_cell].resource_stock * catchability_coefficient

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------- Methods to prompt foraging events ------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def make_choice(self, choice_set):
        """Uses the ChoiceMaker object from choice_making.py to choose a forage choice option
        and gets the actual catch from the choice options"""
        choice_alternative = self.choice_maker.make_choice()                                                            # prompt the ChoiceMaker to choose a choice option based oi the agent memory
        actual_catch = choice_set.discrete_alternatives[choice_alternative].resource_stock \
                       * self.catchability_coefficient                                                                  # read the actual catch an Agent would catch from the choice options themselves rather than and expectation from their memory

        return choice_alternative, actual_catch                                                                         # return the chosen choice option and the real catch as seen from the choice options

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------- Methods to update internal parameters and trackers -----------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def update_agent_trackers(self, alternative_index, catch, time_step_counter):
        """Method to simultaneously update all internal tracker variables of the agent"""
        self.__update_heatmap(alternative_index, catch)                                                                 # update the agent memory of content of a choice options based on catch event
        self.__update_forage_effort_tracker(alternative_index)                                                          # update the agents memory of what choice options were visitied during a simulation
        self.__update_forage_catch_tracker(alternative_index, catch)                                                    # update the agents memory of all catch ever extracted from a choice option
        self.__update_catch(catch)                                                                                      # update the total catch of an agent
        self.__update_time_step_catch(time_step_counter, catch)                                                         # update the catch per time step

    def __update_heatmap(self, alternative_index, catch):
        """overwrites a heatmap choice option entry using the last catch event of the agent"""
        self.heatmap[alternative_index] = catch

    def __update_forage_catch_tracker(self, alternative_index, catch):
        """adds the last catch event of the agent to the choice option total catch gained by the agent considered"""
        self.forage_catch_tracker[alternative_index] += catch

    def __update_forage_effort_tracker(self, alternative_index):
        """updates the effort tracker with the last chosen choice option"""
        self.forage_effort_tracker[alternative_index] += 1

    def __update_catch(self, catch):
        """update agents total catch with last catch event"""
        self.total_catch += catch

    def __update_time_step_catch(self, time_step_counter, catch):
        """update agents time_step specific catch with last catch event"""
        self.time_step_catch[time_step_counter] += catch

    def __update_list_of_knowns(self):  # Quick and dirty way of finding all knowns instead of only adding new ones
        """"make sure the list of knowns is up to date by checking if all choice option indices
        with an entry in the heatmap are also in the list_of_knowns"""
        for alternative in self.heatmap:  # unknowns are alternatives with an integer (0) as catch estimate, not a float
            if isinstance(self.heatmap[alternative], float):
                if alternative not in self.list_of_known_alternatives:
                    self.list_of_known_alternatives.append(alternative)

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------- Methods for information sharing scenarios ------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def share_heatmap_knowledge(self, number_of_alternatives=1):
        """method that returns a given number of alternatives the ForagerAgent has knowledge on
        to be shared with other ForagerAgents"""
        self.__update_list_of_knowns()                                                                                  # make sure the list of known alternatives is up to date
        shared_alternatives_indices = []                                                                                # empty list for later attchment of choice option indices to be shared
        shared_alternatives_data = []                                                                                   # empty list for later attchment of choice option contens to be shared
        if not isinstance(number_of_alternatives, int) and number_of_alternatives != 'ALL':                             # check if number of choice options to be shared is an integer or all
            raise TypeError("number can only be an integer or ALL")

        elif number_of_alternatives == 'ALL':                                                                           # share all data
            shared_alternatives_indices = self.list_of_known_alternatives                                               # to be shared indices are all indices memory has an entry on
            for alternative in shared_alternatives_indices:
                shared_alternatives_data.append(self.heatmap[alternative])                                              # attach all contents of the known choice options 1 by 1 to an empty list

        else:
            alternative_counter = 0
            while alternative_counter < number_of_alternatives:
                shared_alternative = random.choice(self.list_of_known_alternatives)                                     # pick a random choice option index the agents memory has an entry on
                if shared_alternative not in shared_alternatives_indices:                                               # check if we are not already sharing this choice option
                    shared_alternatives_indices.append(shared_alternative)                                              # attach the choice option index from the randomly chosen entry
                    shared_alternatives_data.append(self.heatmap[shared_alternative])                                   # attach the choice option contents from the randmloy chosen entry
                alternative_counter += 1

        return tuple((shared_alternatives_indices, shared_alternatives_data))                                           # return a tuple with choice option indices to be shared and the corresponding contents of those choice options

    def receive_heatmap_knowledge(self, shared_data):
        """updates personal heatmap based on the output from a ForagerAgent().share_heatmap_knowledge() method """
        received_alternative_indices = shared_data[0]                                                                   # get index of shared choice options
        received_alternative_data = shared_data[1]                                                                      # get content of shared choice options

        received_counter = 0
        while received_counter < len(received_alternative_indices):
            # add knowledge if the alternative is unknown
            received_index = received_alternative_indices[received_counter]                                             # get index of a single shared choice option
            received_data = received_alternative_data[received_counter]                                                 # get contents of a single shared choice option
            if isinstance(self.heatmap[received_index], int):                                                           # check if the receiving agent already has an entry for that choice: NO
                self.heatmap[received_index] = received_data                                                            # fill the empty choice option entry with the received data

            # When the receiving agent already has knowledge on the shared knowledge, take the average of both
            elif isinstance(self.heatmap[received_index], float):                                                       # check if the receiving agent already has an entry for that choice: YES
                self.heatmap[received_index] = (received_data + self.heatmap[received_index])/2                         # take average of newly shared data and the information already known from other data

            received_counter += 1                                                                                       # proceed to next shared choice option

        self.__update_list_of_knowns()                                                                                  # update list of known choice options
        # TODO: Functionality for Knowledge degradation


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------- Subclasses of the ForagerAgent object -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class FishermanAgent(ForagerAgent):           # Not Implemented for now
    """specific class to define objects as agents that may forage from a resource.
    Constructed to add functionality specific to agents resembling fishermen.
    Class inherits all functionality from the, more general, ForagerAgent object"""

    def __init__(self):
        ForagerAgent.__init__(self)


class PredatorAgent(ForagerAgent):            # Not Implemented for now
    """specific class to define objects as agents that may forage from a resource.
    Specifically constructed to add functionality specific to agents resembling biological predators.
    Class inherits all functionality from the, more general, ForagerAgent object"""

    def __init__(self):
        ForagerAgent.__init__(self)
