# Make sure the repo root dir is in PYTHONPATH (a hacky solution, until we have a setup script).
import sys
import os
import itertools
import timeit
this_file_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(this_file_dir))

import artemis

start = timeit.default_timer()

# Set inputs.
scenario_file = os.path.join(this_file_dir, 'default_config.yml')  # Config file that needs to be run.
scenario_data = artemis.io.read_data_from_yml(scenario_file)  # Read scenario_file.
output_basefolder = os.path.join(this_file_dir, 'vary_output/')  # Determines output directory.

# Run the simulation for different combinations of parameters.
interference_factors = [0.9, 1.0]
reset_probabilities = [0.0, 0.2]
nbs_receivers = [0, 1]

# for loop over all combinations fo parameter settings
for intfac, resprob, nbrec in itertools.product(interference_factors,reset_probabilities,nbs_receivers):
    # Set parameters.
    scenario_data['competition']['interference_attributes']['interference_factor'] = intfac
    scenario_data['options']['stock_reset']['reset_probability'] = resprob
    agent_name_suffix = ""
    for agent in scenario_data['agents']:
    #    if agent['name'] == "subfleet001":  # In this example, only change nb_receivers for subfleet 1. (remove if statement to adjust values in all agents)
    #        agent['sharing']['receiver_choice']['nb_receivers'] = nbrec
    #        agent_name_suffix += "_" + "SubFleetOne"

        agent['sharing']['receiver_choice'][
        'nb_receivers'] = nbrec  # if changes is wanted in all agents use this one and comment block the above if statement
        agent_name_suffix += "_" + SubFleetAll

    # ensure scenario is being renamed for proper output naming
    scenario_suffix = f'_intfac{intfac}_resprob{resprob}_nbsrec{agent_name_suffix}{nbrec}'
    scenario_data['scenario_id'] = scenario_suffix

    # Set output folder and make sure it exists.
    output_subfolder = os.path.join(output_basefolder, scenario_suffix[1:])
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)

    # Run simulation.
    artemis.run_artemis(scenario_data, output_subfolder, save_config=True)

# time full run of all scenarios
stop = timeit.default_timer()                                                                                           # stop run timer
execution_time = stop - start                                                                                           # calculate elapsed runtime (in seconds)

print("Total Runtime: \t{} seconds".format(str(execution_time)))