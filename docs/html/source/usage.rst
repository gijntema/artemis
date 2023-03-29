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

It is also possible to change parameter values in the python script - for an example, see ``scripts/default_scenario_vary_parameters.py``.
