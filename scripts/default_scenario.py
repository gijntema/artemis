import artemis
import os


# Set inputs.
this_file_dir = os.path.dirname(__file__)
scenario_file = os.path.join(this_file_dir, 'default_config.yml')  # Config file that needs to be run.
output_subfolder = os.path.join(this_file_dir, 'example_output/')  # Determines output directory.

# Run the simulation.
scenario_data = artemis.io.read_data_from_yml(scenario_file)  # Read scenario_file.
artemis.run_artemis(scenario_data, output_subfolder, save_config=False)
