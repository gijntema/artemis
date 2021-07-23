#
# This file is part of ARTEMIS (https://git.wur.nl/ecodyn/XXXX).
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

import random


class AgentSet:                                         # to be implemented, not yet included in the other scripts
    """Class to contain both the agents in ForagerAgent objects (or a more specified version of it)
    and global data on all agents in the model """
    def __init__(self):
        pass
        self.agents = {}                                # dictionary with all agents as ForagerAgent objects
        self.agent_global_tracker = {}                  # forgot why I implemented this and what it means
        self.total_catch = 0                            # Tracker for total catch of all agents and years combined
        self.total_yearly_catch_tracker = {}            # tracker for total catch each year
        self.average_yearly_catch_tracker = {}          # tracker for average catch each year

    def update_agent_trackers(self, agent_id, catch, alternative_index, time_tracker):
        self.agents[agent_id].update_agent_trackers(alternative_index=alternative_index, catch=catch,
                                                   year_counter=time_tracker)

        self.update_total_catch(catch)
        self.update_total_yearly_catch(catch, time_tracker)

    def update_total_catch(self, catch):
        self.total_catch += catch

    def update_average_yearly_catch(self):
        pass

    def update_total_yearly_catch(self, catch, time_tracker):
        self.total_yearly_catch_tracker[str(time_tracker)] += catch

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- the ForagerAgent object -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class ForagerAgent:
    """general class to define objects as agents that may forage from a resource and their attributes"""
    def __init__(self):
        self.forage_catch_tracker = {}                  # tracker variable for total catch gained from each alternative
        self.forage_effort_tracker = {}                 # tracker variable for effort exerted on each alternative
        self.heatmap = {}                               # agents memory on the last forage event in each alternative
        self.total_catch = 0                            # tracker variable to track total catch for this agent
        self.catchability_coefficient = 0               # efficiency of resource uptake of the agent
        self.explore_probability = 0                    # chance an agent chooses a random alternative (when allowed)
        self.id = "no_id"                               # id consistent with other indices used in the rest of the model
        self.yearly_catch = {}                          # tracker variable to check yearly fluctuations in catch
        self.list_of_known_alternatives = []            # list of alternatives that an agent has information on

# --------------------------------------Method to initialize agents before running the main model ----------------------

    def initialize_content(self,
                           choice_set,
                           agent_id,
                           catchability_coefficient,
                           nb_of_alternatives_known,
                           explore_probability):

        # initialise all maps containing data on expectations and results of forage events
        alternative_tracker = 0
        alternative_indices = []
        while alternative_tracker < len(choice_set.discrete_alternatives):
            alternative_id = "alternative_" + str(alternative_tracker)
            self.forage_catch_tracker[alternative_id] = 0           # map with previous yield per alternative
            self.forage_effort_tracker[alternative_id] = 0          # map with previous effort per alternative
            self.heatmap[alternative_id] = 0                        # map with expectations per alternative
            alternative_indices.append(alternative_id)              # construct index list for later use
            alternative_tracker += 1                                # proceed to the next alternative

        # fill heatmap will initial known alternatives
        list_of_knowns = []
        i = 0
        while i < nb_of_alternatives_known:
            # choose a random alternatives that the agent will know
            list_of_knowns.append(random.choice(alternative_indices))
            i += 1                                                  # proceed to generate the next known

        # add the heatmap data for each cell initially known as the catch they would get when fishing there at t=0
        for known_cell in list_of_knowns:
            self.heatmap[known_cell] = \
                choice_set.discrete_alternatives[known_cell].resource_stock * catchability_coefficient

        # include final internal measures of the agent
        self.id = agent_id
        self.catchability_coefficient = catchability_coefficient
        self.explore_probability = explore_probability
        self.list_of_known_alternatives = list_of_knowns

# ----------------------------- Methods to prompt foraging events ------------------------------------------------------

    def forage_maximalization(self, optimalization_method, choice_set):
        # method containing the actual choice of foraging alternative
        if optimalization_method == "BASIC":
            choice_alternative, choice_catch = self.basic_heatmap_optimalization(choice_set)
        else:                                               # Give Error when an unknown optimalization option is chosen
            raise NotImplementedError('optimalization option not yet implemented')

        return choice_alternative, choice_catch

    def forage_random(self, choice_set):
        # forage using a random alternative from the choice set
        alternative_index = random.choice(list(self.heatmap.keys()))
        catch = choice_set.discrete_alternatives[alternative_index].resource_stock * self.catchability_coefficient
        return alternative_index, catch

    def basic_heatmap_optimalization(self, choice_set):
        optimal_catch = 0
        optimal_alternative = 'choice_none'
        for alternative in self.heatmap:
            # discern the catch you would gain according to the information/memory an agent has
            expected_catch = self.heatmap[alternative]
            if expected_catch > optimal_catch:
                optimal_catch = expected_catch
                optimal_alternative = alternative

        actual_catch = choice_set.discrete_alternatives[optimal_alternative].resource_stock\
                       * self.catchability_coefficient

        return optimal_alternative, actual_catch

# ------------------------------- Methods to update internal parameters and trackers -----------------------------------

    def update_agent_trackers(self, alternative_index, catch, year_counter):
        self.update_heatmap(alternative_index, catch)
        self.update_forage_effort_tracker(alternative_index, catch)
        self.update_forage_catch_tracker(alternative_index, catch)
        self.update_catch(catch)
        self.update_yearly_catch(year_counter, catch)

    def update_heatmap(self, alternative_index, catch):
        self.heatmap[alternative_index] = catch

    def update_forage_catch_tracker(self, alternative_index, catch):
        self.forage_catch_tracker[alternative_index] += catch

    def update_forage_effort_tracker(self, alternative_index, catch):
        self.forage_effort_tracker[alternative_index] += 1

    def update_catch(self, catch):
        self.total_catch += catch

    def update_yearly_catch(self, year_counter, catch):
        self.yearly_catch[year_counter] += catch

    def update_list_of_knowns(self):  # Quick and dirty way of finding all knowns instead of only adding new ones
        for alternative in self.heatmap:  # unknowns are alternatives with an integer (0) as catch estimate, not a float
            if isinstance(self.heatmap[alternative], float):
                if alternative not in self.list_of_known_alternatives:
                    self.list_of_known_alternatives.append(alternative)

# --------------------------- Methods for information sharing scenarios ------------------------------------------------

    def share_heatmap_knowledge(self, number_of_alternatives=1):
        """method that returns a given number of alternatives the ForagerAgent has knowledge on
        to be shared with other ForagerAgents"""
        self.update_list_of_knowns()  # make sure the list of known alternatives is up to date
        shared_alternatives_indices = []
        shared_alternatives_data = []
        if not isinstance(number_of_alternatives, int) and number_of_alternatives != 'ALL':
            raise TypeError("number can only be an integer or ALL")

        elif number_of_alternatives == 'ALL':
            shared_alternatives_indices = self.list_of_known_alternatives
            for alternative in shared_alternatives_indices:
                shared_alternatives_data.append(self.heatmap[alternative])

        else:
            alternative_counter = 0
            while alternative_counter < number_of_alternatives:
                shared_alternative = random.choice(self.list_of_known_alternatives)
                if shared_alternative not in shared_alternatives_indices:
                    shared_alternatives_indices.append(shared_alternative)
                    shared_alternatives_data.append(self.heatmap[shared_alternative])
                alternative_counter += 1

        return tuple((shared_alternatives_indices, shared_alternatives_data))

    def receive_heatmap_knowledge(self, shared_data):
        """updates personal heatmap based on the output from a ForagerAgent().share_heatmap_knowledge() method """
        received_alternative_indices = shared_data[0]
        received_alternative_data = shared_data[1]

        received_counter = 0
        while received_counter < len(received_alternative_indices):
            # add knowledge if the alternative is unknown
            received_index = received_alternative_indices[received_counter]
            received_data = received_alternative_data[received_counter]
            if isinstance(self.heatmap[received_index], int):
                self.heatmap[received_index] = received_data

            # When the receiving agent already has knowledge on the shared knowledge, take the average of both
            elif isinstance(self.heatmap[received_index], float):
                self.heatmap[received_index] = (received_data + self.heatmap[received_index])/2

            received_counter += 1

        self.update_list_of_knowns()  # update list of known alternatives


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
