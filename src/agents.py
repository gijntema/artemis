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

class ForagerAgent:
    """general class to define objects as agents that may forage from a resource"""
    def __init__(self):
        self.forage_catch_tracker = {}
        self.forage_effort_tracker = {}
        self.heatmap = {}
        self.total_catch = 0
        self.catchability_coefficient = 0
        self.explore_probability = 0
        self.id = "no_id"

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
            alternative_tracker += 1

        # fill heatmap will initial known alternatives

        list_of_knowns = []
        i = 0
        while i < nb_of_alternatives_known:
            list_of_knowns.append(random.choice(alternative_indices))
            i += 1

        for known_cell in list_of_knowns:
            self.heatmap[known_cell] = \
                choice_set.discrete_alternatives[known_cell].resource_stock * catchability_coefficient

        # include final internal measures of the agent
        self.id = agent_id
        self.catchability_coefficient = catchability_coefficient
        self.explore_probability = explore_probability

    def forage_maximalization(self, optimalization_method):
        if optimalization_method == "BASIC":
            choice_alternative, choice_catch = self.basic_heatmap_optimalization()
        else:
            raise NotImplementedError('optimalization option not yet implemented')

        return choice_alternative, choice_catch

    def forage_random(self, choice_set):
        alternative_index = random.choice(list(self.heatmap.keys()))
        catch = choice_set.discrete_alternatives[alternative_index].resource_stock * self.catchability_coefficient
        return alternative_index, catch

    def basic_heatmap_optimalization(self):
        optimal_catch = 0
        optimal_alternative = 'choice_none'
        for alternative in self.heatmap:
            # discern the catch you would gain according to the heatmap
            catch = self.heatmap[alternative]
            if catch > optimal_catch:
                optimal_catch = catch
                optimal_alternative = alternative

        return optimal_alternative, optimal_catch


    def update_agent_trackers(self, alternative_index, catch):
        self.update_heatmap(alternative_index, catch)
        self.update_forage_effort_tracker(alternative_index, catch)
        self.update_forage_catch_tracker(alternative_index, catch)
        self.update_catch(catch)

    def update_heatmap(self, alternative_index, catch):
        self.heatmap[alternative_index] = catch

    def update_forage_catch_tracker(self, alternative_index, catch):
        self.forage_catch_tracker[alternative_index] += catch

    def update_forage_effort_tracker(self, alternative_index, catch):
        self.forage_effort_tracker[alternative_index] += 1

    def update_catch(self, catch):
        self.total_catch += catch


class FishermanAgent(ForagerAgent):           # empty for now
    """specific class to define objects as agents that may forage from a resource.
    Constructed to add functionality specific to agents resembling fishermen.
    Class inherits all functionality from the, more general, Forager object"""

    pass


class PredatorAgent(ForagerAgent):            # empty for now
    """specific class to define objects as agents that may forage from a resource.
    Specifically constructed to add functionality specific to agents resembling biological predators.
    Class inherits all functionality from the, more general, Forager object"""

    pass
