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
# TODO: ADJUST MODULE DESCRIPTION
# TODO: UNFINISHED MODULE

"""
This Module defines the DynamicsHandler object to change the attributes of the forage options (DiscreteAlternatives)
in the ChoiceSet, e.g. the way a fish stock in a grid cell grows, resets or changes through any other dynamic.

Basic functionality currently supports stock dynamics that reset stock according to a given distribution.
based on the initialisation

the dictionary contains all DiscreteAlternatives as the actual options that are present in a considered system
(e.g. the different grid cells to fish/forage in). Functionality for spatially explicit options can be added
in the child class SpatialGridCell

Module inputs:
-   as key component of the DiscreteAlternative object in choice_set.py the module loads certain attributes
    from said object

Module Usage:
-   the DiscreteAlternative object in choice_set.py uses the DynamicsHandler object to adjust its attributes

Last Updated:
    16-11-2021

Version Number:
    0.1
"""
import random
import numpy as np

class DynamicsHandler:

    def __init__(self, discrete_alternative, dynamics_scenario, **relevant_parameters):
        self.functionality = self.__init_functionality()                                                                # Init dictionary with reference to all functionality, as contained in methods of the class
        self.dynamics = dynamics_scenario                                                                               # assign the way dynamics in foraging options occur (e.g. stock growth, stock reset, changes not related to stock)
        self.relevant_data = {}                                                                                         # initialise an empty data conatiner to store references to the parts of DiscreteAlternative objects needed to function
        self.__init_dynamics(discrete_alternative, **relevant_parameters)                                               # fill the relevant_data with the references needed for functionality

    def __init_functionality(self):
        """defines all functionality through a dictionary with references"""
        functionality = \
            {
                'static':
                    {
                        'init': self.__init_static,
                        'load': 'PLACEHOLDER',
                        'change': 'PLACEHOLDER'
                    },
                'normal_random_repeat':
                    {
                        'init': self.__init_normal_random_repeat,
                        'load': 'PLACEHOLDER',
                        'change': 'PLACEHOLDER'
                    },
                'uniform_random_repeat':
                    {
                        'init': self.__init_uniform_random_repeat,
                        'load': 'PLACEHOLDER',
                        'change': 'PLACEHOLDER'
                    },
                'growth_PLACEHOLDER':
                    {
                        'init': 'PLACEHOLDER',
                        'load': 'PLACEHOLDER',
                        'change': 'PLACEHOLDER'
                    }
            }
        return functionality

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Internal Methods to initialise functionality ---------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __init_dynamics(self, discrete_alternative, **relevant_parameters):
        """Main Functionality method to initialise the dynamics, according to the scenario indicated in self.dynamics"""
        self.functionality[self.dynamics]['init'](discrete_alternative=discrete_alternative, relevant_parameters=relevant_parameters)
        for parameter_key, parameter_reference in relevant_parameters.items():
            self.relevant_data[parameter_key] = parameter_reference

    def __init_static(self, *args):
        pass

    def __init_normal_random_repeat(self, **relevant_parameters):
        self.relevant_data['stock_reset_chance'] = relevant_parameters['stock_reset_chance']
        self.relevant_data['init_stock'] = relevant_parameters['init_stock']
        self.relevant_data['sd_init_stock'] = relevant_parameters['sd_init_stock']
        self.relevant_data['resource_stock'] = relevant_parameters['discrete_alternative'].resource_stock

    def __init_uniform_random_repeat(self, **relevant_parameters):
        self.relevant_data['stock_reset_chance'] = relevant_parameters['stock_reset_chance']
        self.relevant_data['min_stock'] = relevant_parameters['min_stock']
        self.relevant_data['max_stock'] = relevant_parameters['max_stock']
        self.relevant_data['resource_stock'] = relevant_parameters['discrete_alternative'].resource_stock

    def __init_growth_placeholder(self, *args):
        pass

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------ Methods to load data generated during a model run (if applicable) ---------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def load_dynamics_data(self, *args):
        """Main Functionality Method to load adaptive data needed for the dynamics,
        according to the scenario indicated in self.dynamics"""
        pass

    def __load_static(self, *args):
        pass

    def __load_normal_random_repeat(self, *args):
        pass

    def __load_uniform_random_repeat(self, *args):
        pass

    def __load_growth_placeholder(self, *args):
        pass

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------- Methods to load agent choice functionality ----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def change_alternatives(self):
        """Main Functionality Method to prompt dynamics (e.g. stock growth) in DiscreteAlternative Objects to occur,
            according to the scenario indicated in self.dynamics"""
    def __change_static(self):
        pass

    def __change_normal_random_repeat(self):
        if random.random() < self.relevant_data['stock_reset_chance']:
            self.relevant_data['resource_stock'] = self.__pos_normal(mean=self.relevant_data['init_stock'],
                                                                     sd=self.relevant_data['sd_init_stock'])
    def __pos_normal(self, mean, sd):
        """returns values from a normal distribution, cut off at 0, supporting function for other methods """
        x = np.random.normal(loc=mean, scale=sd)
        return x if x > 0 else self.__pos_normal(mean, sd)

    def __change_uniform_random_repeat(self):
        if random.random() < self.relevant_data['stock_reset_chance']:
            self.relevant_data['resource_stock'] = self.__pos_uniform(minimum=self.relevant_data)

    def __pos_uniform(self, minimum, maximum):
        x = np.random.uniform(low=minimum, high=maximum)
        return x if x > 0 else self.__pos_uniform(minimum, maximum)

    def __change_growth_placeholder(self):
        pass


# EOF
