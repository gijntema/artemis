import numpy as np
import random
import artemis
import pandas as pd
import os
pd.set_option("display.precision", 18)


def test_regression_default_scenario():
    """Test if outome of default_config.yml is same as before. Note: the result depends on random number generation
    so this test might fail on a new machine."""

    # Set inputs.
    this_file_dir = os.path.dirname(__file__)
    scenario_file = os.path.join(this_file_dir, 'resources/default_config.yml')  # Config file that needs to be run.
    output_subfolder = os.path.join(this_file_dir, 'test_output/')  # Determines output directory.
    reference_subfolder = os.path.join(this_file_dir, 'resources/')  # Determines reference directory.

    # Run the simulation.
    random.seed(0)  # Make sure we always get the same result.
    np.random.seed(0)  # Make sure we always get the same result.
    scenario_data = artemis.io.read_data_from_yml(scenario_file)  # Read scenario_file.
    artemis.run_artemis(scenario_data, output_subfolder, save_config=False)

    # Make sure the output is the same as it was before.

    # Column 'agent_id' differs but all other data should be the same.
    df1_example = pd.read_csv(os.path.join(output_subfolder, 'flat_time_x_agent_resultsdefault.csv')).drop(['agent_id'], axis=1)
    df1_ref = pd.read_csv(os.path.join(reference_subfolder, 'flat_time_x_agent_resultsdefault.csv')).drop(['agent_id'], axis=1)
    df1_diff = df1_example.compare(df1_ref)
    assert(df1_diff.empty)
    # assert(np.amax(df1_example['average_expected_competitors'].to_numpy() - df1_ref['average_expected_competitors'].to_numpy()) < 1e-8)
    # if not df1_diff.empty:
    #     print(df1_diff)
    print("Agent results passed!")

    # Almost all column names are different here, so we only compare the numerical data.
    df2_example = pd.read_csv(os.path.join(output_subfolder, 'flat_time_x_environment_resultsdefault.csv')).drop(['alternative_id', 'agents_visited'], axis=1)
    df2_ref = pd.read_csv(os.path.join(reference_subfolder, 'flat_time_x_environment_resultsdefault.csv')).drop(['alternative_id', 'agents_visited'], axis=1)
    assert(np.amax(df2_example.to_numpy() - df2_ref.to_numpy()) < 1e-8)
    df2_diff = df1_example.compare(df1_ref)
    if not df2_diff.empty:
        print(df2_diff)
    print("Environment results passed!")


# If you want to run the test function directly.
if __name__ == "__main__":
    test_regression_default_scenario()
