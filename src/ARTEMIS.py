#
# This file is part of ARTEMIS (https://git.wur.nl/ecodyn/artemis.git).
# Copyright (c) 2021 Wageningen Marine Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

# TODO: Update Description Below
"""
This Module is used as the main execution of the model, it is divided into four core aspects:
- Initialize Parameters                         (using scenario file csv and ConfigHandler object)
- Initialize Model                              (make empty objects supporting structure of the model)
- Run Simulations                               (start iteration loop)
    -   Initialize model content                (Use init_objects.ObjectInitializer to set up options and agents in the iteration)
    -   Run Simulation                          (Use run_model.ModelRunner to run an iteration)
    -   extract output data to usable formats   (use DataExtractor to extract Pandas.Dataframe objects with raw data)
- Export Data to datafiles                      (Use DataWriter to create .csv files)

Module inputs:
-   almost all other modules are used directly or indirectly (through one of the other imported modules)

Module Usage:
-   Since this module is the Main, it is used to execute all other modules and is not used by other modules

Last Updated:
    01-10-2021

Version Number:
    0.2
"""

# TODO: replace 'alternatives' with 'choices' or 'options' in all variable, method and function nomenclature -- Potential other name might be ChoiceSet--> Environment (used in computer science) and DiscreteAlternative --> Environment Unit

# ----------------------------------------------------------------------------------------------------------------------
# Import External Modules needed for ARTEMIS functionality
# ----------------------------------------------------------------------------------------------------------------------

import timeit                                                                                                           # Import module to track runtime
start = timeit.default_timer()                                                                                          # Start timer for model run
import pandas as pd                                                                                                     # Pandas dataframes as data structure tool

# ----------------------------------------------------------------------------------------------------------------------
# Import Internal Modules built for ARTEMIS functionality
# ----------------------------------------------------------------------------------------------------------------------

from src.config.init.make_config import ConfigHandler                                                                   # Module to save and access the configuration settings from a simulations scenario config file
from src.config.init.param_to_config_mapping import ParamConverter                                                      # Modules that assigns parameters from ConfigHandler objects a python variable name
from src.run_model import ModelRunner                                                                                   # Module to run the model using initialized agents and choices

from src.tools.model_tools.agents import AgentFleet                                                                     # Module with agents (and groups of agents) functionality
from src.tools.model_tools.choice_set import ChoiceSet                                                                  # Module with choice option (e.g. grid cells) functionality, representing the physical environment agents operate in
from src.tools.model_tools.competition import CompetitionHandler                                                        # Module that handles model feedbacks as a result of competition between agents

from src.tools.output_tools.printing import PrintBlocker                                                                # Module that allows for blocking of print statements in the scripts
from src.tools.output_tools.raw_data_extraction import DataExtractor                                                    # Module to generate output data (as pandas dataframes) from the objects in the model
from src.tools.output_tools.export_data import DataWriter                                                               # Module to write datafiles from the output data

# ----------------------------------------------------------------------------------------------------------------------
# Set up structure for configuration of the model (The ConfigHandler object and the scenario file csv)
# ----------------------------------------------------------------------------------------------------------------------

config_handler = ConfigHandler(scenario_file='base_config_20220120.csv')                                                         # define and load batch file csv containing the parameters for each scenario to run

if len(config_handler.scenarios_config) < 1:
    raise ReferenceError("Config File Contains No Scenarios to Run")                                                    # raise error if scenario file is empty

# ----------------------------------------------------------------------------------------------------------------------
# Set up objects that are independent on simulation settings
# ----------------------------------------------------------------------------------------------------------------------

model_runner = ModelRunner()                                                                                            # initialize the object with the functionality to run a simulation with the initialized agents and choice options
data_extractor = DataExtractor()                                                                                        # initialize the object with the functionality to extract output data from model objects
print_blocker = PrintBlocker()                                                                                          # define object to block printing if desired

# ----------------------------------------------------------------------------------------------------------------------
# Start Looping over the scenarios - parameter and structural configuration/initialisation
# ----------------------------------------------------------------------------------------------------------------------

for scenario in config_handler.scenarios_config:                                                                        # loop over all scanarios read from the batch file csv
    scenario_name = scenario                                                                                            # define tag for scenario name
    print('starting simulations(s) for scenario {}'.format(scenario_name))                                              # print what scenario that is now being run
    output_file_suffix = scenario_name                                                                                  # define current scenario name as suffix to any output file

    # TODO quick and dirty fix based on old structure, can be done better for runtime improvement
    duration, \
    number_of_iterations,\
    reporting,\
    number_of_agents,\
    catchability_coefficient,\
    choice_method,\
    explore_probability,\
    init_number_of_alternatives_known,\
    sharing_strategy,\
    shared_alternatives,\
    no_sharing_attributes,\
    random_sharing_attributes,\
    pick_receiver_strategy,\
    number_of_groups,\
    division_style,\
    group_dynamics,\
    random_choice_attributes,\
    share_partners,\
    receiving_strategy,\
    choice_set_size,\
    growth_type,\
    growth_factor,\
    stock_reset_scenario,\
    chance_reset_stock,\
    min_stock,\
    max_stock,\
    init_stock,\
    sd_init_stock,\
    competition_scenario,\
    interference_factor = \
        ParamConverter().reverse_read_scenario(config_handler=config_handler, scenario_id=scenario_name)                # convert all parameters and settings for the current scenario to the variable names needed

    if not reporting:                                                                                                   # block printing if desired (if reporting is False in a given scenario setting)
        print_blocker.block_print()

    # TODO: Move CompetitionHandler object to run_model.py
    competition_handler = CompetitionHandler(competition_method=competition_scenario,
                                             interference_factor=interference_factor)                                   # object that will ensure competition feedbacks are executed for in the model

    data_writer = DataWriter(output_file_suffix)                                                                        # initialize the object with the functionality to export data files from output data

    time_x_agent_data = pd.DataFrame()                                                                                  # intialize object to contain output data that has data on individual time steps and individual agent
    time_x_environment_data = pd.DataFrame()                                                                            # intialize object to contain output data that has data on individual time steps and environmental units (DiscreteAlternatives or Gridcells)

# ----------------------------------------------------------------------------------------------------------------------
# Start Iteration loop
# ----------------------------------------------------------------------------------------------------------------------
    iteration_counter = 0                                                                                               # initialization of counter for iteration loops
    while iteration_counter < number_of_iterations:
        print('-------------------------------------------------------------------------------------------------------',# print statement for user to keep track of the progression of scenario iterations in the model
              '\nStarting Iteration no.{} \n'.format(str(iteration_counter)),
              "-------------------------------------------------------------------------------------------------------"
              )

# ----------------------------------------------------------------------------------------------------------------------
# initialize the Environment (choice set), containing all discrete alternatives and the fleet, containing all agents
# ----------------------------------------------------------------------------------------------------------------------

        # TODO: Move initialization to run_model.py
        choice_set = ChoiceSet(                                                                                         # initialize the potential options/ environmental units in the model (e.g. the grid with cells to fish in), representing the environment agents operate in
                                nb_alternatives=choice_set_size,
                                stock_distribution=stock_reset_scenario,
                                init_stock=init_stock,
                                sd_init_stock=sd_init_stock,
                                growth_factor=growth_factor,
                                duration=duration, maximum_stock=max_stock, minimum_stock=min_stock
                                )

        fleet = AgentFleet(                                                                                             # initialize the forager agents in the model (e.g. fishermen)
                                nb_agents=number_of_agents,
                                choice_set=choice_set,
                                catchability_coefficient=catchability_coefficient,
                                nb_alternatives_known=init_number_of_alternatives_known,
                                explore_probability=explore_probability,
                                duration_model=duration,
                                choice_method=choice_method,
                                sharing_strategy=sharing_strategy,
                                receiver_choice_strategy=pick_receiver_strategy,
                                receiving_strategy=receiving_strategy,
                                number_of_shared_alternatives=shared_alternatives,
                                number_of_agents_shared_with=share_partners,
                                number_of_sharing_groups=number_of_groups,
                                group_division_style=division_style,
                                group_dynamics=group_dynamics
                                )

# ----------------------------------------------------------------------------------------------------------------------
# RUN SIMULATION
# ----------------------------------------------------------------------------------------------------------------------

        # TODO: Check if returning the ChoiceSet and AgentFleet is necessary, since they seem to be modified in place as well
        choice_set_output, fleet_output = \
            model_runner.run_model(choice_set=choice_set,                                                               # run the model and return final states of the agents and choice options in the model
                                   fleet=fleet,
                                   duration=duration,
                                   stock_reset_scenario=stock_reset_scenario,
                                   init_stock=init_stock,
                                   sd_init_stock=sd_init_stock,
                                   competition_handler=competition_handler,
                                   stock_reset_chance=chance_reset_stock,                                               # TODO: Move  stock_reset chance as internal Attribute of individual DiscreteAlternative Objects, to allow for flexibility
                                   iteration_id=iteration_counter,
                                   max_stock=max_stock,
                                   min_stock=min_stock)

# ----------------------------------------------------------------------------------------------------------------------
# Extract Raw Data in every iteration
# ----------------------------------------------------------------------------------------------------------------------

        time_x_agent_data = \
            time_x_agent_data.append(
                data_extractor.get_time_x_agent_data(agent_set=fleet,
                                                     iteration_id=iteration_counter)).reset_index(drop=True)            # Get Dataframe with data specific per unit of time and agent (e.g. actual catch obtained, competition encountered)

        time_x_environment_data = \
            time_x_environment_data.append(
               data_extractor.get_time_x_environment_data(agent_set=fleet,
                                                          choice_set=choice_set,
                                                          iteration_id=iteration_counter)).reset_index(drop=True)       # Get Dataframe with data specific per unit of time and choice option/environmental subsection (e.g. real stock present, agents catch expectation of each option)

        iteration_counter += 1                                                                                          # progress to the next iteration


# ----------------------------------------------------------------------------------------------------------------------
# Export generated data in every scenario
# ----------------------------------------------------------------------------------------------------------------------

    # ---- exit iteration loop ----

    data_writer.write_csv(time_x_agent_data, 'flat_time_x_agent_results')                                               # write csv output file for data specific per unit of time and agent
    data_writer.write_csv(time_x_environment_data, 'flat_time_x_environment_results')                                   # write csv output file for data specific per unit of time and choice option/environmental subsection

    # Enable Printing
    print_blocker.enable_print()                                                                                        # enable printing to report on runtime and other prints that are always desired regardless of print blocking

    # Progress to next scenario (implicit in code)

# ----------------------------------------------------------------------------------------------------------------------
# Runtime tracking and reporting
# ----------------------------------------------------------------------------------------------------------------------

# ---- exit scenario loop ----

stop = timeit.default_timer()                                                                                           # stop run timer
execution_time = stop - start                                                                                           # calculate elapsed runtime (in seconds)

print("Model Runtime: \t{} seconds".format(str(execution_time)))                                                        # report runtime in seconds

# EOF
