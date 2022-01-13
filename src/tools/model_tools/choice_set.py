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
This Module is used to define (the characteristics of) options any ForagerAgent may choose from during a module run,
examples of choices are:
- which grid cell to fish/forage in
- what forage search tactic to employ
- what prey/target species to choose

basic functionality of the model currently is mostly geared towards fishery (spatial) options, but model structure
allows for future implementations of other types of options.

characteristics general to all choice options (DiscreteAlternative Objects)
and a list of choices (in dictionary format) are added as part of the ChoiceSet object

the dictionary contains all DiscreteAlternatives as the actual options that are present in a considered system
(e.g. the different grid cells to fish/forage in). Functionality for spatially explicit options can be added
in the child class SpatialGridCell

Module inputs:
-   the parameters form init_param.py are used to load the characteristics in any ChoiceSet object

Module Usage:
-   init_objects.py uses the module to initialize all objects needed at any later stage in the model
-   run_model.py uses the module to execute choice set operations
-   agents.py uses the module to create a mirror of the choice set to map acquired information on

Last Updated:
    06-09-2021

Version Number:
    0.1
"""

import numpy as np
import copy
from collections import defaultdict
from src.tools.model_tools.resource_dynamics import DynamicsHandler

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------- Objects to contain the full choice set -----------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class ChoiceSet:
    """Class to contain all data for a given choice set of alternatives,
    including the choice options in the choice set as DiscreteAlternative objects in a dictionary object"""

    # initialisation of the object defining the attributes of a choice set
    def __init__(self, nb_alternatives, stock_distribution, init_stock, sd_init_stock, minimum_stock, maximum_stock, growth_factor=1, duration=1):
        self.discrete_alternatives = {}                                                                                 # dictionary with all choice options as DiscreteAlternative objects
        self.effort_map = {}                                                                                            # tracker variable for effort (effort = 1 -> a single forage event) exerted to each choice options
        self.catch_map = {}                                                                                             # tracker variable for total catch gained from each choice options
        self.time_visit_map = defaultdict(dict)
        self.stock_time_tracker = defaultdict(dict)

        self.__init_attributes(nb_alternatives=nb_alternatives, stock_distribution=stock_distribution,
                               init_stock=init_stock, sd_init_stock=sd_init_stock, growth_factor=growth_factor,
                               duration=duration, maximum_stock=maximum_stock, minimum_stock=minimum_stock)

    def __init_attributes(self, nb_alternatives, stock_distribution, init_stock, sd_init_stock, minimum_stock, maximum_stock, growth_factor, duration):
        alternative_tracker = 0
        while alternative_tracker < nb_alternatives:                                                                    # loop the creation of a alternative for the full size of the considered set of choices possibel
            alternative_id = "alternative_" + str(alternative_tracker).zfill(len(str(nb_alternatives)))                 # assign ID
            self.discrete_alternatives[alternative_id] = DiscreteAlternative(alternative_id, stock_distribution=stock_distribution,init_stock=init_stock,
                                                                                   minimum_stock=minimum_stock,
                                                                             maximum_stock=maximum_stock
                                                                             , sd_init_stock=sd_init_stock, growth_factor=growth_factor)        # define a single choice option with an ID, initial stock (with an sd) and growth factor
            self.effort_map[alternative_id] = 0                                                                         # define a tracker with 0 effort on each choice option
            self.catch_map[alternative_id] = 0                                                                          # define a tracker with 0 catch on every effort
            self.time_visit_map[alternative_id] = dict()

            duration_counter = 0                                                                                        # make counter for all time_steps in the model for While loop functioning
            while duration_counter < duration:                                                                          # loop over all time steps in the model
                time_id = str(duration_counter).zfill(len(str(duration)))
                self.time_visit_map[alternative_id][time_id] = 0
                duration_counter += 1
            alternative_tracker += 1                                                                                    # proceed to next choice_option

    def update_environmental_stock_tracker(self, time_id):
        for alternative in self.discrete_alternatives:
            stock = copy.deepcopy(self.discrete_alternatives[alternative].resource_stock)
            self.stock_time_tracker[time_id][alternative] = stock


class SpatialChoiceSet(ChoiceSet):                                                                                      # placeholder for future functionality
    """Class to represent a spatially explicit ChoiceSet,
    more specific version of the ChoiceSet object, inheriting all functionality from the ChoiceSet,
    but leaving room for spatial aspects of the Choice set"""

    def __init__(self):             # placeholders for later use
        self.grid = None
        ChoiceSet.__init__(self)

    def load_grid(self):            # placeholders for later use with real world data
        pass

    def load_alternatives(self):    # placeholders for later use with real world data
        pass


# ----------------------------------------------------------------------------------------------------------------------
# --------------------- Objects to contain a single choice options in a discrete choice set ----------------------------
# ----------------------------------------------------------------------------------------------------------------------

class DiscreteAlternative:
    """Class to contain the choice option specific aspects and modifications,
    for now only resource stock is included"""

    def __init__(self, alternative_id=None, stock_distribution='uniform_random_repeat', init_stock=100, sd_init_stock=25, minimum_stock=0, maximum_stock=100, growth_factor=1):
        """"function defining the content of a choice options (e.g. a single grid cell in spatial considerations)"""
        self.alternative_id = alternative_id                                                                            # id consistent with other indices used in the rest of the model
        self.resource_stock = 0                                                                                         # contains the value(s) for the stock present
        self.growth_factor = 1                                                                                          # initialise value for growth factor
        self.initialize_standard_stock(stock_distribution=stock_distribution, init_stock=init_stock, sd_init_stock=sd_init_stock, minimum_stock=minimum_stock, maximum_stock=maximum_stock, growth_factor=growth_factor)                                        # loads proper initialization, overwriting the stock and growth factor with specified values
        self.stock_type = 'singular'                                                                                    # indicates the structure of the stock (e.g. singular/age class)
        self.stock_growth_type = 'exponential'                                                                          # indicator for the way the stock grows
        #self.dynamics_handler = DynamicsHandler(self, dynamics_scenario=stock_distribution)

    def initialize_standard_stock(self, stock_distribution, init_stock, sd_init_stock, minimum_stock, maximum_stock, growth_factor=1):
        """draws and sets an initial stock size in the choice option drawn from
        a normal distribution with a given  mean and sd"""
        if stock_distribution == 'normal_random_repeat':
            self.resource_stock = self.__pos_normal(mean=init_stock, sd=sd_init_stock)                                  # generate random stock with given mean and standard deviation from a normal distribution
            self.growth_factor = growth_factor                                                                          # set growth factor (in dynamic stock scenarios)

        elif stock_distribution == 'uniform_random_repeat':
            self.init_uniform_standard_stock(minimum_stock=minimum_stock, maximum_stock=maximum_stock)
            self.growth_factor = growth_factor

    def __pos_normal(self, mean, sd):
        """returns values from a normal distribution, cut off at 0 """
        x = np.random.normal(loc=mean, scale=sd)
        return x if x > 0 else self.__pos_normal(mean, sd)

    def init_uniform_standard_stock(self, minimum_stock, maximum_stock):
        self.resource_stock = self.__pos_uniform(minimum_stock, maximum_stock)
        print('new, reset, stock value is {}'.format(self.resource_stock))

    def __pos_uniform(self, minimum, maximum):
        x = np.random.uniform(low=minimum, high=maximum)
        return x if x > 0 else self.__pos_uniform(minimum, maximum)

    def stock_growth(self):
        """Method placeholder for future implementation of dynamic stock, currently not great executed"""
        # TODO: Assess if this hopelessly outdated and incomplete method needs to be removed or salvaged for later use.
        #  functionality probably should be contained in a functionality dictionary (see e.g. CompetitionHandler object)
        if self.stock_type == 'singular' and self.stock_growth_type == 'exponential':                                   # placeholder for stock growth, hopelessly outdated for now
            self.__resource_stock_growth_exp()

    def resource_stock_harvest(self, resource_uptake):
        """Method placeholder for future implementation of more dynamic stocks"""
        self.resource_stock -= resource_uptake

    def __resource_stock_growth_exp(self):
        """Method placeholder for future implementation of dynamic stock, currently not great executed"""
        self.resource_stock = self.resource_stock * self.growth_factor


class SpatialGridCell(DiscreteAlternative):                                 # for future use
    """"Extension of the DiscreteAlternative class to include
    spatially explicit attributes of a discrete alternative object,
    all functionality from the DiscreteAlternative class is inherited"""

    def __init__(self):

        """placeholder for future initialisation of this subclass, inheritance of functionality is already defined"""
        DiscreteAlternative.__init__(self)                                                                              # inherit functionality of parent class DiscreteAlternative
        self.location = (float('nan'), float('nan'))                                                                    # placeholder to define spatial attrbutes of the choice options


