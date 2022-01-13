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
This Module allows for functionality in turning on or off printing during the running of the model of ARTEMIS.py

Module inputs:
-   True/False flag from init_param.py

Module Usage:
-   use dby ARTEMIS.py to turn on or off printing

Last Updated:
    07-10-2021

Version Number:
    0.1
"""

import sys
import os

class PrintBlocker:
    """ Class to enable or disable the execution of print statements in scripts"""

    def block_print(self):
        """"blocks printing until the method enable_print is executed"""
        sys.stdout = open(os.devnull, 'w')

    def enable_print(self):
        """"allows for printing again, removes the effect of method block_printing"""
        sys.stdout = sys.__stdout__
