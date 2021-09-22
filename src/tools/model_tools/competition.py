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

# TODO: Implement further functionality, only interference and absent competition supported now
"""
This Module is aimed at handling and executing any corrections or effects of competition
using the CompetitionHandler object

this module is read by run_model.py to be used to correct any profits or catches through competition

Module inputs:
depending on the method of competition
-   outputs from choice_maker.py, specifically the ChoiceMaker.make_choice method
-   outputs from agents.py, specifically the ForagerAgent.make_choice module
-   pooled outputs from the above

Module Usage:
-   the module will be used in run_model.py to introduce competition in simulations

Last Updated:
    07-09-2021

Version Number:
    0.1
"""

from collections import defaultdict, OrderedDict
from math import exp


class CompetitionHandler:
    """class to implement competition mechanisms / feedbacks in the model"""
# TODO: init and load are now for all methods duplicates of each other for quick fix, consider if this is needed
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------ Dictionary dictating all functionality ------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __init__(self, competition_method):
        self.competition_instruction = self.__init_instructions()
        self.competition_method = competition_method
        self.relevant_data = self.__init_relevant()

    def __init_instructions(self):
        """define a dictionary with instruction on all possible functionality for including competition"""

        instructions = {
            'absent':                                                                                                   # competition is not modelled
                {
                    "init": self.__init_absent,
                    "load": self.__load_absent,
                    "correct": self.__correct_absent,

                },
            'interference-simple':                                                                                      # competition through interference in accounted for by correcting the catch for the amount agents that have chosen that choice option
                {
                    "init": self.__init_interference,
                    "load": self.__load_interference,
                    "correct": self.__correct_interference_simple
                },
            'uptake':                                                                                                   # competition is modelled through resource uptake, leaving less for other agents
                {   # UNSUPPORTED
                    "init": self.__init_uptake,
                    "load": self.__load_uptake,
                    "correct": self.__correct_uptake
                },
            'price-simple':                                                                                             # competition is modelled for human agents by correcting the sale prices with the total catch
                {   # UNSUPPORTED
                    "init": self.__init_price,
                    "load": self.__load_price,
                    "correct": self.__correct_price_simple
                },
            'fixed-catch':
                {
                    # relic code= obsolete
                    "init": self.__init_fixed_catch,
                    "load": self.__load_fixed_catch,
                    "correct": self.__correct_fixed_catch
                }
            # Enter future functionality HERE
        }

        return instructions
# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Internal Methods to initialise functionality ---------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __init_relevant(self):
        """method to initialise the relevant attributes needed for competition corrections"""
        if isinstance(self.competition_method, str):                                                                    # if only a single competition type is specified
            relevant = self.__init_relevant_single()
        elif isinstance(self.competition_method, tuple):                                                                # if multiple competition types are specified - currently not supported
            relevant = self.__init_relevant_multiple()
        else:
            raise TypeError("competition definition is only allowed as string or tuple")                                # if competition is specified in an unsupported format

        return relevant

    def __init_relevant_single(self):
        """method to initialise the relevant attributes needed for competition corrections (when only 1 scenario)"""
        relevant = self.competition_instruction[self.competition_method]['init']()
        return relevant

    def __init_relevant_multiple(self):
        """method to initialise the relevant attributes needed for competition corrections (when multiple scenarios)"""
        # TODO -- FUTURE -- allow functionality for multiple scenarios simultaneously - METHOD UNFINISHED
        relevant = {}
        # Include loop here to ensure relevant data for all considered competition are added
        return relevant

    def __init_absent(self):
        """method to define relevant data, as an absent competition does not need any data,
         only present to fix bugging"""
        relevant_data = dict()
        relevant_data['effort_tracker'] = defaultdict(int)                                                              # dictionary that creates and returns an integer 0 if a key is called that is not already in
        relevant_data['agent_choices'] = OrderedDict()                                                                  # OrderedDict as the order of the uptake matters (resources might be depleted by other before an agent arrives
        return relevant_data

    def __init_interference(self):
        """method to initialise a tracker for effort, as effort is used a basis to correct catch for interference"""
        relevant_data = dict()
        relevant_data['effort_tracker'] = defaultdict(int)                                                              # dictionary that creates and returns an integer 0 if a key is called that is not already in
        relevant_data['agent_choices'] = OrderedDict()                                                                  # OrderedDict as the order of the uptake matters (resources might be depleted by other before an agent arrives
        return relevant_data

    def __init_uptake(self):
        """method to initialise an ordered tracker for catch, as catch is used to reduce the resource stock"""
        relevant_data = dict()
        relevant_data['effort_tracker'] = defaultdict(float)                                                            # dictionary that creates and returns a float 0.0 if a key is called that is not already in
        relevant_data['agent_choices'] = OrderedDict()                                                                  # OrderedDict as the order of the uptake matters (resources might be depleted by other before an agent arrives
        return relevant_data

    def __init_price(self):
        """method to initialise a tracker for catch of the current time_unit,
        as catch is used a basis to correct the price of foraged goods. making this competition method only applicable
        to human forager agents"""
        relevant_data = dict()
        relevant_data['effort_tracker'] = defaultdict(float)                                                            # dictionary that creates and returns a float 0.0 if a key is called that is not already in
        relevant_data['agent_choices'] = OrderedDict()                                                                  # OrderedDict as the order of the uptake matters (resources might be depleted by other before an agent arrives
        return relevant_data

    def __init_fixed_catch(self):
        relevant_data = dict()
        relevant_data['effort_tracker'] = defaultdict(float)                                                            # dictionary that creates and returns a float 0.0 if a key is called that is not already in
        relevant_data['agent_choices'] = OrderedDict()                                                                  # OrderedDict as the order of the uptake matters (resources might be depleted by other before an agent arrives
        return relevant_data

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------- Methods to load relevant agent choices functionality ------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def load_competition_data(self, chosen_alternative_id, agent_id, interference_factor=0):
        """loads data on the agent and chosen choice option"""
        self.competition_instruction[self.competition_method]['load'](chosen_alternative_id, agent_id, interference_factor)

    def __load_absent(self, chosen_alternative_id, agent_id, interference_factor=0):
        """loads data on the agent and chosen choice option"""
        self.relevant_data['effort_tracker'][chosen_alternative_id] += 1                                                # add agents chocie to overall predicted effort distribution
        self.relevant_data['agent_choices'][agent_id] = chosen_alternative_id                                           # remember what agent choose which choice option

    def __load_interference(self, chosen_alternative_id, agent_id, interference_factor=0.8):
        """loads data on the agent and chosen choice option"""
        self.relevant_data['effort_tracker'][chosen_alternative_id] += 1                                                # add agents chocie to overall predicted effort distribution
        self.relevant_data['agent_choices'][agent_id] = chosen_alternative_id                                           # remember what agent choose which choice option
        self.relevant_data['interference_factor'] = interference_factor

    def __load_uptake(self, chosen_alternative_id, agent_id, interference_factor=0):
        """Placeholder --> Functionality currently not supported"""
        pass

    def __load_price(self, chosen_alternative_id, agent_id):
        """Placeholder --> Functionality currently not supported"""
        pass

    def __load_fixed_catch(self, chosen_alternative_id, agent_id, interference_factor=0):
        """loads data on the agent and chosen choice option"""
        self.relevant_data['effort_tracker'][chosen_alternative_id] += 1                                                # add agents chocie to overall predicted effort distribution
        self.relevant_data['agent_choices'][agent_id] = chosen_alternative_id
# ----------------------------------------------------------------------------------------------------------------------
# ---------------------- Methods to return any corrections needed to account for competition ---------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def competition_correction(self, choice_set, agent_set, agent_id, time_id):
        """returns the real catch a ForagerAgent gains, when corrected for competition"""

        choice_id = self.relevant_data['agent_choices'][agent_id]

        uncorrected_catch = choice_set.discrete_alternatives[choice_id].resource_stock \
                            * agent_set.agents[agent_id].catchability_coefficient                                       # extract hypothetical catch if competition was absent

        corrected_catch, correction_tag = \
            self.competition_instruction[self.competition_method]['correct'](choice_id, uncorrected_catch)              # correct hypothetical catch using the competition methods specified

        print(
            "{} is foraging in {} and is hindered by interference with {}".format(agent_id, choice_id, correction_tag)  # report on interference to user
            )

        agent_set.update_agent_trackers(agent_id, corrected_catch, choice_id, time_id)                                  # update trackers on the agents
        # agent_set.update_memory
        choice_set.catch_map[choice_id] += corrected_catch                                                              # update tracker of the choice set for total catch in a choice option
        choice_set.effort_map[choice_id] += 1                                                                           # update tracker of the choice set for effort in a choice option

        if 'uptake' in self.competition_method:
            choice_set.discrete_alternatives[choice_id].resource_stock_harvest(corrected_catch)                         # quick and dirty fix of blocking out the piece of code that reduces the resource stoc

    def __correct_absent(self, choice_id, uncorrected_catch):
        """empty function to prevent errors, does not correct catch in any way but adds a tag"""
        corrected_catch = uncorrected_catch                                                                             # don't correct data, purely for visual aid to what happens
        correction_tag = "<absent_competition>"                                                                         # output expects a tag for interference, default given as interference is not presnet in this scenario
        return corrected_catch, correction_tag

    def __correct_interference_simple(self, choice_id, uncorrected_catch):
        """method to correct catch using interference by using the interference factor
        as percentual decline of catch per competitor"""
        number_of_competitors = self.relevant_data['effort_tracker'][choice_id]                                         # identify how many competitors forage in the same choice from the tracker variables
        corrected_catch = uncorrected_catch * (self.relevant_data['interference_factor']^(number_of_competitors-1))     # correct using interference fatctro^(number_competitors-1), prone to errors if called when 0 competitors are present, this should however not be possible
        correction_tag = str(number_of_competitors-1) + " other foragers"
        return corrected_catch, correction_tag

    def __correct_fixed_catch(self, choice_id, uncorrected_catch):
        """method to correct catch by dividing over the number of competitors, creates very strong competition"""
        number_of_competitors = self.relevant_data['effort_tracker'][choice_id]                                         # identify how many competitors forage in the same choice from the tracker variables
        corrected_catch = uncorrected_catch / number_of_competitors                                                     # prone to DividedByZeroError, but as this method should never be called if no foraging occurs in a choice option, this should be a nice test for functioning
        correction_tag = str(number_of_competitors - 1) + " other foragers"                                             # generate interference tag for later use in reporting
        return corrected_catch, correction_tag

    def __correct_uptake(self, choice_id, uncorrected_catch):
        """Placeholder --> Functionality currently not supported -- future planned resource uptake as competition"""
        pass

    def __correct_price_simple(self, choice_id, uncorrected_catch):
        """Placeholder --> Functionality currently not supported -- future planned market price change as competition"""
        pass

# ----------------------------------------------------------------------------------------------------------------------
# --------------------- Methods to reset the saved content to start from default relevant data--------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def reset_relevant_data(self):
        """full reset of the relevant data trackers to ensure this will not interfere
        with competition handling in the next time_step"""
        self.relevant_data = self.__init_relevant()                                                                     # Reinitialise relevant data


