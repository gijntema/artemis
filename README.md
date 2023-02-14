# ARTEMIS model

## Introduction
The Agents in Resource Tracking and Extracting Model for Information Strategies (ARTEMIS) 
is a general investigation into the role of informed decision making 
in strategies of human or biological agents in foraging or extracting resources. 
Examples include food foraging or commercial fishing.

## Requirements
	* Python 3.9.4+
	* Git

see `requirements.txt` for python packages and versions employed


## Getting Started

### Install Python and a Python interpreter (e.g. PyCharm)
* Python : https://www.python.org/downloads/
* Pycharm : https://www.jetbrains.com/pycharm/


### Clone remote repository ARTEMIS to a local git repository
First make sure you have git installed from; https://git-scm.com/

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

### Create virtual environment
Depends on the interpreter chosen (should be adjusted to include several interpreters)


## Using the model

### Install packages

Enter into terminal:

```
pip install -r requirements.txt 
```

### Adjust initial parameters (if not running the basic version of the model)
Open `examples/default_config.yml` and enter desired parameters defined there.
More information on the correct variables to be used per scenario at **docs/input_descriptions.md** and  **docs/*_schema.md**.

### Starting the model
Run `python examples/default_scenario.py`. 
For a script that does some parameter variation, see `examples/default_scenario_vary_parameters.py`

### Tips for adjusting the Model
Please realise that a testing framework **tests/test_functionality.py** is present to test if any adjustments hinder 
the functionality of the model. New functionality test can also be included in this framework. Simply run the script 
to test the functionality **OUTDATED SHOULD BE CHECKED FOR FUNCTIONALITY**.

### Profiling the code

```
python -m cProfile -o profiling.txt scripts/default_scenario.py
python -m pstats profiling.txt
profiling.txt% sort cumulative
profiling.txt% stats 30
```
