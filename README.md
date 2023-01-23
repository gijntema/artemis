# ARTEMIS model

## Introduction
The Agents in Resource Tracking and Extracting Model for Information Strategies (ARTEMIS) 
is a general investigation into the role of informed decision making 
in strategies of human or biological agents in foraging or extracting resources. 
Examples include food foraging or commercial fishing.

## Requirements
	* Python 3.9.4+
	* Git

see src/package_versions.txt for python packages and versions employed


## Getting Started

### Install Python and a Python interpreter (e.g. PyCharm)
* Python : https://www.python.org/downloads/
* Pycharm : https://www.jetbrains.com/pycharm/


### Clone remote repository ARTEMIS to a local git repository
First make sure you have git installed from; https://git-scm.com/

Define the desired local location of the model

    $ cd \<desired project directory>\ARTEMIS

clone the remote repository into the defined location:

(Using https):

    $ git clone https://git.wur.nl/ecodyn/artemis.git

or

(Using SSH key):

    $ git clone git@git.wur.nl:ecodyn/artemis.git

### Create virtual environment
Depends on the interpreter chosen (should be adjusted to include several interpreters)


## Using the model

### Install packages

Enter into terminal:

    $ pip install -r src/package_versions.txt 


### Adjust initial parameters (if not running the basic version of the model)
Create a .csv file (**base_config.csv** is a template) to define the correct variables to be used per scenario, see **src/input_descriptions.md** 
for descriptions of the different variables that can be adjusted

### Starting the model
open src/ARTEMIS.py and define .csv file that contains defined input variables (**line 72**)
run **src/ARTEMIS.py**

### Tips for adjusting the Model
Please realise that a testing framework **tests/test_functionality.py** is present to test if any adjustments hinder 
the functionality of the model. New functionality test can also be included in this framework. Simply run the script 
to test the functionality **OUTDATED SHOULD BE CHECKED FOR FUNCTIONALITY**
