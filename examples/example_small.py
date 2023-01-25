# Make sure the repo root dir is in PYTHONPATH (a hacky solution, until we have a setup script).
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
from src.ARTEMIS import run_artemis

# Input / output.
scenario_file = 'example_config.csv'  # Config file that needs to be run
output_subfolder = '../../../examples/example_output/' # determines that the output should be written to a subfolder in the regular output folder (if not define output_subfolder = '')

# Run the simulation.
np.random.seed(0)  # Make sure we always get the same result.
run_artemis(scenario_file, output_subfolder)

# Make sure the output is the same as it was before.
df1_example = pd.read_csv('example_output/flat_time_x_agent_resultsdefault.csv')
df1_ref = pd.read_csv('reference_output/flat_time_x_agent_resultsdefault.csv')
print(df1_example.compare(df1_ref))
df2_example = pd.read_csv('example_output/flat_time_x_environment_resultsdefault.csv')
df2_ref = pd.read_csv('reference_output/flat_time_x_environment_resultsdefault.csv')
print(df2_example.compare(df2_ref))
