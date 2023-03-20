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
        if not "pytest" in sys.modules:  # To prevent pytest error "OSError: [WinError 6] The handle is invalid"
            sys.stdout = open(os.devnull, 'w')

    def enable_print(self):
        """"allows for printing again, removes the effect of method block_printing"""
        if not "pytest" in sys.modules:  # To prevent pytest error "OSError: [WinError 6] The handle is invalid"
            sys.stdout = sys.__stdout__
