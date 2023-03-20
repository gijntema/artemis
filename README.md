# ARTEMIS model

## Introduction
The Agents in Resource Tracking and Extracting Model for Information Strategies (ARTEMIS) 
is a general investigation into the role of informed decision making 
in strategies of human or biological agents in foraging or extracting resources. 
Examples include food foraging or commercial fishing.

## Getting Started

### Clone ARTEMIS repository

First make sure you have git installed from; https://git-scm.com/.

Define the desired local location of the model

```
cd \<desired project directory>\ARTEMIS
```

clone the remote repository into the defined location:

(Using https):

```
git clone https://git.wur.nl/ecodyn/artemis.git
```

or

(Using SSH key):

```
git clone git@git.wur.nl:ecodyn/artemis.git
```

Alternatively, you can use a git client with a GUI like GitHub Desktop.

### Installation

Make sure you have python 3.9.4+ installed (https://www.anaconda.com/ or https://www.python.org/downloads/)

Then, if you use windows, go to the repository root directory and type in a command prompt:

```
python -m venv venv
.\venv\Scripts\activate
pip install -e .
```

Or on linux:

```
python -m venv venv
. venv/bin/activate
pip install -e .
```

### Running the example scripts
Make sure you are in the correct virtual environment. To activate it,
run `.\venv\Scripts\activate`. Then, run `python scripts/default_scenario.py`. 
Output should be written to `scripts/example_output`.

For a script that does some parameter variation, see `scripts/default_scenario_vary_parameters.py`.

### Make your own ARTEMIS scripts
To adjust initial parameters (if not running the basic version of the model), copy `scripts/default_config.yml` and
rename it to start your own parameter file. Open the copy in your editor of choice (we recommend PyCharm) and enter desired parameters defined there.
More information on the correct variables to be used per scenario at **docs/input_descriptions.md** and  **docs/*_schema.md**.

A `yml` parameter file can be read and run with a python script:

```python
import artemis
import os

# Set inputs/outputs.
scenario_file = "path/to/your_parameter_file.yml"
output_subfolder = "path/where/you/want/your/output"

# Run the simulation.
scenario_data = artemis.io.read_data_from_yml(scenario_file)  # Read scenario_file.
artemis.run_artemis(scenario_data, output_subfolder, save_config=False)  # Run artemis.
```

It is also possible to change parameter values in the python script - for an example, see `scripts/default_scenario_vary_parameters.py`.

### Testing

Please realise that a testing framework `tests/test_*.py` is present to test if any adjustments hinder 
the functionality of the model. New functionality test can also be included in this framework.

To run the tests, again make sure you are in the correct virtual environment. 
Then run the command `pytest` (or if that does not work run `python -m pytest`). 
To see stdout output, add the `-s` option, or run the test 
scripts directly without using pytest.

### Profiling the code

To get profiling results, you can run:

```
python -m cProfile -o profiling.txt scripts/default_scenario.py
python -m pstats profiling.txt
profiling.txt% sort cumulative
profiling.txt% stats 30
```

## License

Copyright (c) 2021 Wageningen Marine Research

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.