# TODO: Implement further functionality, only interference and absent competition supported now
"""
This Module is aimed at handling and executing any effects of competition on effort and catch
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
    01-10-2021

Version Number:
    0.1
"""

from collections import defaultdict, OrderedDict
from sys import exit
import copy

class CompetitionHandler:
    """class to implement competition mechanisms / feedbacks in the model"""
# TODO: init and load are now for all methods duplicates of each other for quick fix, consider if this is needed
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------ Dictionary dictating all functionality ------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __init__(self, competition_method, interference_factor):
        """"initialize competition """
        self.competition_instruction = self.__init_instructions()
        self.competition_method = competition_method
        self.relevant_data = self.__init_relevant()
        self.relevant_data['interference_factor'] = interference_factor

    def __init_instructions(self):
        """define a dictionary with instruction on all possible functionality for including competition"""

        instructions = {
            'absent':                                                                                                   # competition is not modelled
                {
                    "init": self.__init_absent,
                    "load": self.__load_absent,
                    "correct": self.__correct_absent,

                },
            'interference-simple':                                                                                      # competition through interference accounted for by correcting the effort for the number of agents that have chosen that choice option
                {
                    "init": self.__init_interference,
                    "load": self.__load_interference,
                    "correct": self.__correct_interference_simple
                },

            'split-catch':
                {
                    # relic code = obsolete
                    "init": self.__init_split_catch,
                    "load": self.__load_split_catch,
                    "correct": self.__correct_split_catch
                }
            # Enter future functionality HERE
        }

        return instructions
# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Internal Methods to initialise functionality ---------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __init_relevant(self):
        """method to initialise the relevant attributes (e.g. competition specific trackers),
        needed when accounting for competition"""
        if isinstance(self.competition_method, str):                                                                    # if only a single competition type is specified
            relevant = self.__init_relevant_single()
        elif isinstance(self.competition_method, tuple):                                                                # if multiple competition types are specified - currently not supported
            relevant = self.__init_relevant_multiple()
        else:
            raise TypeError("competition definition is only allowed as string or tuple \n"
                            "competition is currently defined as {} of type {}".format(self.competition_method,
                                                                                       type(self.competition_method)))                                # if competition is specified in an unsupported format

        return relevant

    def __init_relevant_single(self):
        """method to initialise the relevant attributes (e.g. competition specific trackers)
         needed when accounting for a single competition type of competition"""
        relevant = self.competition_instruction[self.competition_method]['init']()
        return relevant

    # UNIMPLEMENTED FOR FUTURE USE OF MULTIPLE COMPETITION EFFECTS SIMULTANEOUSLY
    def __init_relevant_multiple(self): # TODO KW: write down the difference between _single and _multiple
        """method to initialise the relevant attributes (e.g. competition specific trackers)
         needed when accounting for multiple competition types"""
        # TODO -- FUTURE -- allow functionality for multiple scenarios simultaneously - METHOD UNFINISHED
        relevant = {}
        # Include loop here to ensure relevant data for all considered competition are added
        return relevant

    def __init_absent(self): # TODO: specify relevant data!
        """method to define relevant data: effort and choice; when there is no competition,
         only present to fix bugging"""
        relevant_data = dict()
        relevant_data['effort_tracker'] = defaultdict(int)                                                              # dictionary that creates and returns an integer 0 if a key is called that is not already in
        relevant_data['agent_choices'] = dict()
        return relevant_data

    def __init_interference(self):
        """method to initialise a tracker for effort and choice, because effort is used a basis to correct catch for interference"""
        relevant_data = dict()
        relevant_data['effort_tracker'] = defaultdict(int)                                                              # dictionary that creates and returns an integer 0 if a key is called that is not already in
        relevant_data['agent_choices'] = dict()
        return relevant_data


    def __init_split_catch(self):
        """method to initialise a function for splitting the catch"""
        relevant_data = dict()
        relevant_data['effort_tracker'] = defaultdict(float)                                                            # dictionary that creates and returns a float 0.0 if a key is called that is not already in
        relevant_data['agent_choices'] = dict()                                                                 # OrderedDict as the order of the uptake matters (resources might be depleted by other before an agent arrives
        return relevant_data

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------- Methods to load agent choice functionality -------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def load_competition_data(self, chosen_alternative_id, agent_id, interference_factor=None):                          # TODO: Migrate interference factor to relevant data and remove hardcoded data
        """main functionality method for loading data on the agent and chosen choice option""" # TODO which data is loaded?
        if interference_factor is None:
            interference_factor=self.relevant_data['interference_factor']
        self.competition_instruction[self.competition_method]['load'](chosen_alternative_id, agent_id, interference_factor)

    def __load_absent(self, chosen_alternative_id, agent_id, interference_factor):
        """loads data on the agent and chosen choice option"""  # TODO check if all comments are unique
        self.relevant_data['effort_tracker'][chosen_alternative_id] += 1                                                # add agents chocie to overall predicted effort distribution
        self.relevant_data['agent_choices'][agent_id] = chosen_alternative_id                                           # remember what agent choose which choice option

    def __load_interference(self, chosen_alternative_id, agent_id, interference_factor):
        """loads data on the agent and chosen choice option"""
        self.relevant_data['effort_tracker'][chosen_alternative_id] += 1                                                # add agents chocie to overall predicted effort distribution
        self.relevant_data['agent_choices'][agent_id] = chosen_alternative_id                                           # remember what agent choose which choice option
#        self.relevant_data['interference_factor'] = interference_factor                                                 # TODO: migrate interference factor to initialisation of relevant data
                                                                                                                        # TODO DOUBLE CHECK FOR DUPLICATE FUNCTIONALITY

    def __load_split_catch(self, chosen_alternative_id, agent_id, interference_factor):
        """loads data on the agent and chosen choice option""" #TODO KW: specify which data
        self.relevant_data['effort_tracker'][chosen_alternative_id] += 1                                                # add agents chocie to overall predicted effort distribution
        self.relevant_data['agent_choices'][agent_id] = chosen_alternative_id

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------- Methods to return any adjustments needed to account for competition ---------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def competition_correction(self, choice_set, agent_set, agent_id, time_id):
        """Main Functionality Method, returns the real catch a ForagerAgent gains, when adjusted for competition"""

        choice_id = self.relevant_data['agent_choices'][agent_id]

        uncorrected_catch = copy.deepcopy(choice_set.discrete_alternatives[choice_id].resource_stock) \
                            * agent_set.agents[agent_id].catchability_coefficient                                       # extract hypothetical catch if competition was absent

        corrected_catch, competitors_encountered, correction, hypothetical_correction = \
            self.competition_instruction[self.competition_method]['correct'](choice_id, uncorrected_catch)              # correct hypothetical catch using the competition methods specified


        # update agent Trackers
        agent_set.update_agent_trackers(agent_id, corrected_catch, choice_id, time_id)                                  # update trackers on the agents itself
        agent_set.update_uncorrected_catch_tracker(time_id=time_id, agent_id=agent_id,
                                                   uncorrected_catch=uncorrected_catch)
        agent_set.update_corrected_catch_tracker(time_id=time_id, agent_id=agent_id,
                                                 corrected_catch=corrected_catch)
        agent_set.update_realised_competition_tracker(time_id=time_id, agent_id=agent_id,
                                                      realised_competition=competitors_encountered)

        # Update grid cell trackers
        choice_set.catch_map[choice_id] += corrected_catch                                                              # update tracker of the choice set for total catch in a choice option
        choice_set.effort_map[choice_id] += 1                                                                           # update tracker of the choice set for effort in a choice option
        choice_set.time_visit_map[choice_id][time_id] += 1

    def update_choice_set_competition_trackers(self, choice_set, time_id):
        for choice_id in choice_set.discrete_alternatives:
            corrected_catch, competitors_encountered, correction, hypothetical_correction = \
                self.competition_instruction[self.competition_method]['correct'](choice_id, uncorrected_catch=1)

            choice_set.competition_correction[time_id][choice_id] = correction
            choice_set.hypothetical_competition_correction[time_id][choice_id] = hypothetical_correction

    def __correct_absent(self, choice_id, uncorrected_catch):
        """empty function to prevent errors, does not correct catch in any way but adds a tag"""
        corrected_catch = uncorrected_catch                                                                             # don't correct data, purely for visual aid to what happens
        competitors_encountered = -99                                                                                   # output expects a tag for interference, default given as interference is not presnet in this scenario
        correction = 1
        theoretical_correction = 1
        return corrected_catch, competitors_encountered, correction, theoretical_correction

    def __correct_interference_simple(self, choice_id, uncorrected_catch):
        """method to correct catch using interference by using the interference factor
        as percentual decline of catch per competitor"""
        number_of_competitors = self.relevant_data['effort_tracker'][choice_id]                                         # identify how many competitors forage in the same choice from the tracker variables
        competitors_encountered = number_of_competitors - 1

        correction = self.relevant_data['interference_factor'] ** competitors_encountered
        hypothetical_correction = self.relevant_data['interference_factor'] ** number_of_competitors
        corrected_catch = uncorrected_catch * correction                                                                # correct using interference fatctro^(number_competitors-1), prone to errors if called when 0 competitors are present, this should however not be possible

        return corrected_catch, competitors_encountered, correction, hypothetical_correction

    def __correct_split_catch(self, choice_id, uncorrected_catch):
        """method to correct catch by dividing over the number of competitors, creates very strong competition"""
        number_of_competitors = self.relevant_data['effort_tracker'][choice_id]                                         # identify how many competitors forage in the same choice from the tracker variables
        correction = 1/number_of_competitors
        hypothetical_correction = 1/(number_of_competitors + 1)

        corrected_catch = uncorrected_catch * correction                                                                # prone to DividedByZeroError, but as this method should never be called if no foraging occurs in a choice option, this should be a nice test for functioning
        competitors_encountered = number_of_competitors - 1                                                             # generate interference tag for later use in reporting
        return corrected_catch, competitors_encountered, correction, hypothetical_correction


# ----------------------------------------------------------------------------------------------------------------------
# --------------------- Methods to reset the saved content to start from empty relevant data--------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def reset_relevant_data(self): #TODO: add the relevant data explicitly
        """full reset of the relevant data trackers to ensure this will not interfere
        with competition handling in the next time_step"""
        self.relevant_data = self.__init_relevant() | {'interference_factor': self.relevant_data['interference_factor']}                                                                     # Reinitialise relevant data


# EOF