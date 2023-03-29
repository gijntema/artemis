Usage
=====

Running the example scripts
###########################

Make sure you are in the correct virtual environment. To activate it,
run (on Windows) ``.\venv\Scripts\activate``. Then, run ``python scripts/default_scenario.py``. 
Output should be written to ``scripts/example_output``.

For a script that does some parameter variation, see ``scripts/default_scenario_vary_parameters.py``.

Make your own ARTEMIS scripts
#############################

To adjust initial parameters (if not running the basic version of the model), copy ``scripts/default_config.yml`` and
rename it to start your own parameter file. Open the copy in your editor of choice (we recommend PyCharm) and enter desired parameters defined there.
More information on the correct variables to be used per scenario at `input format <input_format.html>`_.

A ``yml`` parameter file can be read and run with a python script: ::

    import artemis
    import os

    # Set inputs/outputs.
    scenario_file = "path/to/your_parameter_file.yml"
    output_subfolder = "path/where/you/want/your/output"

    # Run the simulation.
    scenario_data = artemis.io.read_data_from_yml(scenario_file)  # Read scenario_file.
    artemis.run_artemis(scenario_data, output_subfolder, save_config=False)  # Run artemis.

It is also possible to change parameter values in the python script, for example: ::

    import os
    import itertools
    import artemis


    # Set inputs.
    scenario_file = "path/to/your_parameter_file.yml"
    output_basefolder = "path/where/you/want/your/output"

    # Run the simulation for different combinations of parameters.
    interference_factors = [0.9, 1.0]
    reset_probabilities = [0.0, 0.2]
    nbs_receivers = [0, 1]

    # Loop over all combinations of parameter settings.
    scenario_data = artemis.io.read_data_from_yml(scenario_file)  # Read scenario_file.
    for intfac, resprob, nbrec in itertools.product(interference_factors, 
                                                    reset_probabilities, 
                                                    nbs_receivers):
        # Set parameters.
        scenario_data['competition']['interference_attributes']['interference_factor'] = intfac
        scenario_data['options']['stock_reset']['reset_probability'] = resprob
        agent_name_suffix = ""
        for agent in scenario_data['agents']:
            agent['sharing']['receiver_choice']['nb_receivers'] = nbrec

        # Ensure unique output naming.
        scenario_suffix = f'_intfac{intfac}_resprob{resprob}_nbsrec{nbrec}'
        scenario_data['scenario_id'] += scenario_suffix

        # Set output folder and make sure it exists.
        output_subfolder = os.path.join(output_basefolder, scenario_suffix[1:])
        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)

        # Run simulation.
        artemis.run_artemis(scenario_data, output_subfolder, save_config=True)
