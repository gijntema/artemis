Installation
============

Cloning the repository
######################

First make sure you have git installed from; https://git-scm.com/.

Define the desired local location of the model ::

    cd \<desired project directory>\ARTEMIS

clone the remote repository into the defined location (using https): ::

    git clone https://git.wur.nl/ecodyn/artemis.git

or (using SSH key): ::

    git clone git@git.wur.nl:ecodyn/artemis.git

Alternatively, you can use a git client with a GUI like GitHub Desktop.

Installing the Python code
##########################

Make sure you have python 3.9.4+ installed (https://www.anaconda.com/ or https://www.python.org/downloads/)

Then, if you use windows, go to the repository root directory and type in a command prompt: ::

    python -m venv venv
    .\venv\Scripts\activate
    pip install -e .

Or on linux: ::

    python -m venv venv
    . venv/bin/activate
    pip install -e .
