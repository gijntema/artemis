# Make sure the repo root dir is in PYTHONPATH (a hacky solution, until we have a setup script).
import sys
import os
import itertools
this_file_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(this_file_dir))

import numpy as np
import pandas as pd
import random
import artemis


# Set inputs
scenario_file = os.path.join(this_file_dir, 'default_config.yml')  # Config file that needs to be run
scenario_data = artemis.io.read_data_from_yml(scenario_file)  # Read scenario_file.
output_basefolder = os.path.join(this_file_dir, 'vary_output/') # Determines output directory

# Run the simulation for different combinations of parameters.
interference_factors = [0.9, 1.0]
reset_probabilities = [0.0, 0.2]
nbs_receivers = [0, 1]
for intfac, resprob, nbrec in itertools.product(interference_factors, reset_probabilities, nbs_receivers):

    # Set parameters.
    scenario_data['competition']['interference_attributes']['interference_factor'] = intfac
    scenario_data['options']['stock_reset']['reset_probability'] = resprob
    for agent in scenario_data['agents']:
        agent['sharing']['receiver_choice']['nb_receivers'] = nbrec

    # Set output folder and make sure it exists.
    dirname = f'intfac{intfac}_resprob{resprob}_nbsrec{nbrec}'
    output_subfolder = os.path.join(output_basefolder, dirname)
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)

    # Run simulation.
    artemis.run_artemis(scenario_data, output_subfolder, save_config=True)
