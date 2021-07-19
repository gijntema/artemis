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

# Module usable to define the exogenous variables of any ARTEMIS run

# Forager Characteristics
explore_probability = 0.2           # probability a forager does not choose a known cell, but picks a random cell
catchability_coefficient = 0.2      # proportional uptake of the resource stock in one foraging event

# Resource characteristics
init_stock = 100                    # mean of initial stock present
sd_init_stock = 25                  # standard deviation of initial stock present
init_number_of_alternatives_known = 4   # number of alternatives each agents knows at initialisation
growth_factor = 2                   # per time step growth of stock

# model characteristics
duration = 20                       # amount of time steps in the model
choice_set_size = 20                # amount of discrete alternatives in the choice set
amount_of_agents = 100              # amount of foragers in the model


