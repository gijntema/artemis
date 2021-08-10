# ARTEMIS model

## Introduction
The Agents in Resource T. Extraction Model for Information Strategies (ARTEMIS) is a general investigation the role of informed decision making in strategies of human or biological agents in foraging or extracting resources. 
Examples include food foraging or commercial fishing.

## Requirements
	* Python 3.9.4+
	* Git

see package_versions.txt for python packages and versions employed


## Getting Started

### Install Python and a Python interpreter (e.g. PyCharm)
* Python : https://www.python.org/downloads/
* Pycharm : https://www.jetbrains.com/pycharm/


### Clone remote repository ARTEMIS to a local git repository
First make sure you have git installed.

https://git-scm.com/

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

Enter into console:

    $ pip install -r package_versions.txt 


### Adjust initial parameters (if not running the basic version of the model)
Open **src/config/init_param.py** and enter desired parameters defined there

### Starting the model
run **src/ARTEMIS.py**

### Tips for adjusting the Model
Please realise that a testing framework **tests/test_functionality.py** is present to test if any adjustments hinder 
the functionality of the model. New functionality test can also be included in this framework
