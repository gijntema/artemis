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
    01-10-2021

Version Number:
    0.2
"""



import random
import copy
from collections import defaultdict  # TODO: --STRUCTURAL-- Replace difficult initialisation
from src.tools.model_tools.choice_making import ChoiceMaker


class AgentSet:                                         # to be implemented, not yet included in the other scripts
    """Class to contain both the agents in ForagerAgent objects (or a more specified version of it)
    and global data on all agents in the model """
    def __init__(self):
        self.agents = {}                                # dictionary with all agents as ForagerAgent objects
        self.total_catch = 0                            # Tracker for total catch of all agents and time_steps combined
        self.total_time_step_catch_tracker = {}         # tracker for total catch each time_step
#        self.time_step_catch_distribution = {}         # tracker to save distribution of catch over the agents for every time_step - Currently not used
        self.average_expected_competitor_tracker = defaultdict(dict)   # tracker to contain the average expected amount of competitors expected when picking any cell

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

    def update_memory_trackers(self, time_id):
        for agent in self.agents:
            self.agents[agent].update_memory_trackers(time_id)

    def update_average_expected_competitor_tracker(self, time_id):
        """Method that updates a tracker containing data on the average number of competitors expected
        in a given time step for every agent"""

        temp_probability_dictionary = {}                                                                                # temporary dictionary to store agent specific probability maps fro choosing a option (e.g. grid cell) to forage in/from
        number_of_options = len(self.agents[next(iter(self.agents))].heatmap)                                           # get total number of options(e.g. the amount of grid cells an agent can choose from) as the number of entries in the first agents heatmap

        for agent in self.agents:                                                                                       # Loop over Agents (1) to transform an agent heatmap into a prbability map --> what is the chance an agent will i each option
            agent_data = self.agents[agent]                                                                             # define agent data to keep the script visually pleasing
            sum_heatmap_entries = sum(agent_data.heatmap.values())                                                      # calculate sum of heatmap entries fro later use
            probability_of_exploration = agent_data.explore_probability                                                 # get probability of picking a random option for late ruse

            probability_map = copy.deepcopy(agent_data.heatmap)                                                         # create copy of heatmap to overwrite with new data (still contains the regular heatmap entries, but ensures same data structure)
            for entry in probability_map:                                                                               # loop over all entries in an agents heatmap to transform memory catch data into probabilities of choosing that option
                probability_map[entry] /= sum_heatmap_entries                                                           # divide heatmap entries by sum of entries to gain proportional weights as probability of choosing an option
                probability_map[entry] *= (1-probability_of_exploration)                                                # correct for the fact that probability of choosing an option based on the heatmap is not 100%
                probability_map[entry] += probability_of_exploration/number_of_options                                  # add the chance of choosing the option at random through exploration

            temp_probability_dictionary[agent] = copy.deepcopy(probability_map)                                         # make entry for currently considered agent in dictionary of probability maps and load constructed probability map

        for agent_i in temp_probability_dictionary:                                                                     # Loop over Agents (2): calculate the expected encounters for each agent, when considering their choice probabilities-- this is NOT internalised in an agent decision making process, merely used as descriptive statistic
            cumulative_encounters_expected = 0                                                                          # initialize cumulative tracker for expected encounters in options for foraging
            for entry in temp_probability_dictionary[agent_i]:                                                          # loop over the newly acquired probabilities of choosing each option
                for agent_j in temp_probability_dictionary:                                                             # loop over Agents (3): pairwise comparisons of the chance of encountering any potential competitors j (other agents)
                    if agent_i != agent_j:                                                                              # disregard the chance of meeting oneself
                        encounter_chance = \
                            temp_probability_dictionary[agent_i][entry] * \
                            temp_probability_dictionary[agent_j][entry]                                                 # chance at meeting in the considered option: Pi,k,t,real * Pj,k,t,real

                        cumulative_encounters_expected += encounter_chance                                              # add the pairwise expected encounters to the cumulative expected competitors
            average_encounters_expected = cumulative_encounters_expected / number_of_options                            # divide cumulative tracker by number of options --> Cexp,i,t

            self.average_expected_competitor_tracker[time_id][agent_i] = average_encounters_expected                    # add the calculated measure to overall tracker in the agent_set as tracker[time=t][agent=i] = Cexp,i,t


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- the ForagerAgent object -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class ForagerAgent:
    """general class to define objects as agents that may forage from a resource and their attributes"""
    def __init__(self, choice_set, choice_method, agent_id=None,
                 catchability_coefficient=0, nb_of_alternatives_known=1, explore_probability=0):

        # Tracker variables
        self.total_catch = 0                                                                                            # tracker variable to track total catch for this agent
        self.forage_catch_tracker = {}                                                                                  # tracker variable for total catch gained from each alternative
        self.forage_effort_tracker = {}                                                                                 # tracker variable for total location visits on each alternative (visits per alternative, cumulative for all time_steps)
        self.time_step_catch = {}                                                                                       # tracker variable to check time_step fluctuations in catch
        self.knowledge_evolution_tracker = defaultdict(dict)                                                            # tracker to identify how the memory of an agent changes over time

        # basic attributes/parameters
        self.id = agent_id                                                                                              # id consistent with other indices used in the rest of the model
        self.catchability_coefficient = catchability_coefficient                                                        # efficiency of resource uptake of the agent
        self.explore_probability = explore_probability                                                                  # chance an agent chooses a random alternative (when allowed)

        # Memory attributes
        self.heatmap = {}                                                                                               # agents memory on the last forage event in each alternative
        self.list_of_known_alternatives = \
            self.__initialize_list_of_knowns(choice_set=choice_set,
                                            nb_of_alternatives_known=nb_of_alternatives_known)                          # list of alternatives that an agent has information on
        self.__initialize_fill_heatmap(choice_set=choice_set)                                                           # initialise the heatmap

        # Decision Making attribute
        self.choice_maker = ChoiceMaker(choice_set=choice_set,                                                          # object that identifies/loads the relevant data from ForagerAgents and can make foraging decisions for ForagerAgents based on that data
                                        choice_method=choice_method,
                                        agent=self)


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------- Method to initialize agents before running the main model --------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    # TODO Potential to make more efficient using collections.defaultdict()?
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

    def __initialize_list_of_knowns(self, nb_of_alternatives_known, choice_set):
        """initialises a list of #(nb_of_alternatives_known) choice option indices to
        simulate what choice options have already been foraged in before the start of a simulation"""
        choice_set_length = len(choice_set.discrete_alternatives)                                                       # identify number of choice options
        alternative_indices = self.__initialize_choice_set_mirrors(choice_set_length)                                   # generate list of all choice option indices

        list_of_knowns = []
        i = 0                                                                                                           # counter to track loop with
        while i < nb_of_alternatives_known:                                                                             # loop to generate all knowns choice options
            # choose a random alternatives that the agent will know
            new_known = random.choice(alternative_indices)                                                              # choose a random
            if new_known not in list_of_knowns:                                                                         # check if the option is not already in the list of knowns to ensure each agents gets to know 4 options
                list_of_knowns.append(new_known)                                                                        # attach the new known to the list of knowns
                i += 1                                                                                                  # proceed to generate the next known choice option, only happens if the random generated known is really attached

        return list_of_knowns                                                                                           # return list of initial known choice options of an Agent

    def __initialize_fill_heatmap(self, choice_set):
        """use the list of known choice options to fill the expected catches in the memory of the agent"""
        for known_cell in self.list_of_known_alternatives:
            self.heatmap[known_cell] = \
                choice_set.discrete_alternatives[known_cell].resource_stock * self.catchability_coefficient

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------- Methods to prompt foraging events ------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def make_choice(self, choice_set):
        """Uses the ChoiceMaker object from choice_making.py to choose a forage choice option
        and gets the actual catch from the choice options"""
        choice_alternative = self.choice_maker.make_choice()                                                            # prompt the ChoiceMaker to choose a choice option and retrun the ID of the chosen choice options
        self.__update_list_of_knowns()
        return choice_alternative                                                                                       # return the chosen choice option

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------- Methods to update internal parameters and trackers -----------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def update_agent_trackers(self, alternative_index, catch, time_step_counter):
        """Method to simultaneously update all internal tracker variables of the agent"""
        self.__update_heatmap(alternative_index, catch)                                                                 # update the agent memory of content of a choice options based on catch event
        self.__update_forage_effort_tracker(alternative_index)                                                          # update the agents memory of what choice options were visitied during a simulation
        self.__update_forage_catch_tracker(alternative_index, catch)                                                    # update the agents memory of all catch ever extracted from a choice option
        self.__update_catch(catch)                                                                                      # update the total catch of an agent
        self.__update_time_step_catch(time_step_counter, catch, alternative_index)                                                         # update the catch per time step

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

    def __update_time_step_catch(self, time_step_counter, catch, alternative_id):
        """update agents time_step specific catch with last catch event"""
        if catch is float(0):
            exit('Corrected Catch yields 0 for <{}>, with catchability <{}> in choice option <{}>time <{}>'
                 .format(self.id,
                         self.catchability_coefficient,
                         alternative_id,
                         time_step_counter))
        self.time_step_catch[time_step_counter] += catch

    def __update_list_of_knowns(self):  # Quick and dirty way of finding all knowns instead of only adding new ones
        """"make sure the list of knowns is up to date by checking if all choice option indices
        with an entry in the heatmap are also in the list_of_knowns"""
        for alternative in self.heatmap:  # unknowns are alternatives with an integer (0) as catch estimate, not a float
            if isinstance(self.heatmap[alternative], float):
                if alternative not in self.list_of_known_alternatives:
                    self.list_of_known_alternatives.append(alternative)

    def update_memory_trackers(self, time_id):
        """currently ERRORS""" #TODO CURRENTLY does not work properly (all knowns for agent x are always an age of x)
        for known in self.list_of_known_alternatives:

            try:
                time_of_origin = self.knowledge_evolution_tracker[time_id][known]
            except KeyError:
                time_of_origin = -1

            temp_data = {
                        'time_of_origin': time_of_origin
                        }                                                                                               # empty entry for now, can contain such data as age_of_knowledge or discount factor of knowledge (age specific corrections in expectations)
            temp_data['age_of_knowledge'] = int(time_id) - 1 - temp_data['time_of_origin']
            self.knowledge_evolution_tracker[time_id][known] = temp_data

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------- Methods for information sharing scenarios ------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def share_heatmap_knowledge(self, number_of_alternatives=1):
        """method that returns a given number of alternatives the ForagerAgent has knowledge on
        to be shared with other ForagerAgents"""
        print("<{}> is now starting to share data".format(self.id))
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

    def receive_heatmap_knowledge(self, shared_data, time_id=-99):
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

            # TODO: duplicate functionality with self.update_memory_trackers()
            # attempted functionality for knowledge degredation and knowledge age trackers (how long ago did an agent obtain a heatmap entry)
#            try:
#                self.knowledge_evolution_tracker[time_id][received_index]['time_of_origin'] = int(time_id)              # test if a time_of_origin us already present, and if so replace with the current time

#            except KeyError:
#                self.knowledge_evolution_tracker[time_id][received_index] = dict()                                      # if time_o
#                self.knowledge_evolution_tracker[time_id][received_index]['time_of_origin'] = int(time_id)

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
