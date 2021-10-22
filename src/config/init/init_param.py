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
This Module is aimed at defining all parameter values and scenarios used in the model,

this module is read by ARTEMIS.py to determine all parameter variables and scenarios.

Module inputs:
-   None

Module Usage:
-   all defined variables are input for module ARTEMIS.py

Last Updated:
    01-10-2021

Version Number:
    0.1
"""

# Module usable to define the exogenous variables of any ARTEMIS run
# TODO: eventually change this module to read the specified information form a configuration file (e.g. .json file)

# Forager Characteristics
explore_probability = 0.2                   # probability a forager does not choose a known cell, but picks a random cell
catchability_coefficient = 0.2              # proportional uptake of the resource stock in one foraging event
init_number_of_alternatives_known = 4       # number of choice options each agents has information on at initialisation
choice_method = 'explore_weighted_heatmap'  # defines the way an agent chooses what forage option to forage from

# Resource characteristics
init_stock = 100                    # mean of initial stock present
sd_init_stock = 25                  # standard deviation of initial stock present
growth_factor = 1                   # per time step growth of stock (1 represents a static population in current Default settings)


# model characteristics
duration = 100                          # number of time steps in the model
choice_set_size = 20                    # number of discrete alternatives in the choice set
number_of_agents = 100                  # number of foragers in the model
number_of_iterations = 10                # number of iterations/simulations the model runs for

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- GROWTH SCENARIO PARAMETERS -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
growth_type = 'static'                  # indicates stock dynamics -- placeholder, currently not implemented
stock_reset_scenario = 'random-repeat'  # indicates if and how the stock in a DiscreteAlternative objects resets
chance_reset_stock = 0.9                # chance the stock is repeated at the end of a time_step

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- INFORMATION SHARING PARAMETERS -------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
sharing_strategy = 'random_sharing'                 # determines what an agent will share
pick_receiver_strategy = 'random_choice'            # determines with whom an agent will share
receiving_strategy = "combine_receiver"             # determines how a receiver agent will handle shared data

# Quantitative Parameters
shared_alternatives = 1                 # number of known alternatives shared at any given time
share_partners = 1                     # the number of agents an agent informs about a (part of) the personal heatmap


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- COMPETITION PARAMETERS ------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

competition_scenario = 'interference-simple'  # indicate the way competition is modelled in the model
interference_factor = 0.8                     # indicates the reduction in catch for every competitor present

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------- Reporting Settings -------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
reporting = True                            # flag to turn on or off print reporting during the model runs

