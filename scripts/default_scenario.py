# Make sure the repo root dir is in PYTHONPATH (a hacky solution, until we have a setup script).
import sys
import os
this_file_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(this_file_dir))

import numpy as np
import pandas as pd
import random
import artemis


# Set inputs.
scenario_file = os.path.join(this_file_dir, 'default_config.yml')  # Config file that needs to be run.
output_subfolder = os.path.join(this_file_dir, 'example_output/')  # Determines output directory.
reference_subfolder = os.path.join(this_file_dir, 'reference_output/')  # Determines reference directory.

# Run the simulation.
random.seed(0)  # Make sure we always get the same result.
np.random.seed(0)  # Make sure we always get the same result.
scenario_data = artemis.io.read_data_from_yml(scenario_file)  # Read scenario_file.
artemis.run_artemis(scenario_data, output_subfolder, save_config=False)

# Make sure the output is the same as it was before.

# Column 'agent_id' differs but all other data should be the same.
df1_example = pd.read_csv(os.path.join(output_subfolder, 'flat_time_x_agent_resultsdefault.csv')).drop(['agent_id'], axis=1)
df1_ref = pd.read_csv(os.path.join(reference_subfolder, 'flat_time_x_agent_resultsdefault.csv')).drop(['agent_id'], axis=1)
assert(df1_example.compare(df1_ref).empty)

# Almost all column names are different here, so we only compare the numerical data.
df2_example = pd.read_csv(os.path.join(output_subfolder, 'flat_time_x_environment_resultsdefault.csv')).drop(['alternative_id', 'agents_visited'], axis=1)
df2_ref = pd.read_csv(os.path.join(reference_subfolder, 'flat_time_x_environment_resultsdefault.csv')).drop(['alternative_id', 'agents_visited'], axis=1)
assert(np.amax(df2_example.to_numpy() - df2_ref.to_numpy()) < 1e-8)
