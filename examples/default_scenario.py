# Make sure the repo root dir is in PYTHONPATH (a hacky solution, until we have a setup script).
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
import random
from src.ARTEMIS import run_artemis


# Set inputs
scenario_file = 'default_config.yml'  # Config file that needs to be run
output_subfolder = '../../../examples/example_output/' # determines that the output should be written to a subfolder in the regular output folder (if not define output_subfolder = '')

# R=un the simulation
random.seed(0)  # Make sure we always get the same result.
np.random.seed(0)  # Make sure we always get the same result.
run_artemis(scenario_file, output_subfolder)

# Make sure the output is the same as it was before.

# Column 'agent_id' differs but all other data should be the same.
df1_example = pd.read_csv('example_output/flat_time_x_agent_resultsdefault.csv').drop(['agent_id'], axis=1)
df1_ref = pd.read_csv('reference_output/flat_time_x_agent_resultsdefault.csv').drop(['agent_id'], axis=1)
assert(df1_example.compare(df1_ref).empty)

# Almost all column names are different here, so we only compare the numerical data.
df2_example = pd.read_csv('example_output/flat_time_x_environment_resultsdefault.csv').drop(['alternative_id', 'agents_visited'], axis=1)
df2_ref = pd.read_csv('reference_output/flat_time_x_environment_resultsdefault.csv').drop(['alternative_id', 'agents_visited'], axis=1)
assert(np.amax(df2_example.to_numpy() - df2_ref.to_numpy()) < 1e-8)
