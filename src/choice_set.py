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

import numpy as np


# ----------------------------- Objects to contain the full choice set -------------------------------------------------
class ChoiceSet:
    def __init__(self):
        self.discrete_alternatives = {}

    def load_standard_alternatives(self, s):
        return s


    def load_observed_alternatives(self, dataset):
        pass


class SpatialChoiceSet(ChoiceSet):

    def __init__(self):
        self.grid = None
        ChoiceSet.__init__(self)

    def load_grid(self):
        pass

    def load_alternatives(self):
        pass


# --------------------- Objects to contain individual alternatives in a discrete choice set ----------------------------
class DiscreteAlternative:

    def __init__(self):
        self.resource_stock = 0

    def initialize_standard_stock(self, init_stock, sd_init_stock):
        self.resource_stock = np.random.normal(loc=init_stock, scale=sd_init_stock)

    def resource_stock_harvest(self, resource_uptake):
        self.resource_stock -= resource_uptake


class SpatialGridCell(DiscreteAlternative):         # for future use

    def __init__(self):
        DiscreteAlternative.__init__(self)
        self.location = [float('nan'), float('nan')]


