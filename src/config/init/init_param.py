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

# Module usable to define the exogenous variables of any ARTEMIS run
# TODO: eventually change this module to read the specified information form a configuration file (e.g. .json file)

# Forager Characteristics
explore_probability = 0.2           # probability a forager does not choose a known cell, but picks a random cell
catchability_coefficient = 0.2      # proportional uptake of the resource stock in one foraging event
init_number_of_alternatives_known = 4   # number of alternatives each agents knows at initialisation


# Resource characteristics
init_stock = 100                    # mean of initial stock present
sd_init_stock = 25                  # standard deviation of initial stock present
growth_factor = 1                   # per time step growth of stock (1 represents a static population currently)


# model characteristics
duration = 50                       # amount of time steps in the model
choice_set_size = 100               # amount of discrete alternatives in the choice set
amount_of_agents = 20               # amount of foragers in the model
number_of_iterations = 500           # amount of iterations the model runs for

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- GROWTH SCENARIO PARAMETERS -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
growth_type = 'static'              # indicates stock dynamics
stock_reset_scenario = 'random-repeat' # indicates if an how the stock in a DiscreteAlternative resets/
chance_repeat_stock = 0.2           # chance the same stock as the previous time step is present

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- INFORMATION SHARING PARAMETERS -------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
information_sharing_scenario = 'Random Sharing'
# considered functionality: ['No Sharing', Coalition Sharing', 'Random Sharing']

# Indicators 'Random Sharing'
share_partners = 1       # the amount of agents an agent informs about a (part of) the personal heatmap
shared_alternatives = 1                 # amount of known alternatives shared at any given time

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- UNIMPLEMENTED FUNCTIONALITY PLANNED FOR FUTURE --------------------------
# ----------------------------------------------------------------------------------------------------------------------

# information Sharing Scenario Indicators
# information_sharing_scenario = 'No Sharing'

information_sharing_method = 'Shared Heatmap'
# considered functionality: ['Shared Heatmap, Information Diffusion']
# TODO: Implement shared heatmap functionality

# Indicators 'Coalition Forming'
coalition_cheaters = False              # indicates the existence of cheaters (agents that are part of multiple groups)
coalition_size = amount_of_agents/10    # indicates the size of the coalition (in number of agent members)
# TODO: Implement Coalitions in Knowledge Sharing
