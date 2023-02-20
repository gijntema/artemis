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

"""
This Module is aimed at extracting data and measures from unusable data formats and currently functions to:
-   extract raw data from the objects AgentSet, ForagerAgent, ChoiceSet and DiscreteAlternative
-   calculate aggregate measures based on the raw data extracted from objects
-   transform the model output into usable (raw) data formats: pandas.Dataframe objects for plotting and saving

Module inputs:
-   No Modules
-   Module only works on objects defined in the modules agents.py and choice_set.py

Module Usage:
-   methods of the DataExtractor object are used in ARTEMIS.py to write output data,
    outputs generated there are then used as input for export_data.py to write .csv data files

Last Updated:
    04-01-2021

Version Number:
    0.1
"""

# import external packages
import pandas as pd
from collections import defaultdict

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------ Main Functionality Method -------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class DataExtractor:
    """" Restructures the raw data outputs from the model to a usable data format (a pandas.Dataframe object)"""
    def __init__(self):
        """initialisation method: make a functionality dictionary,
        only for future functionality/flexibility,
        aids runtime and readability"""

        self.functionality_extraction = self.__init_functionality_extraction()                                          # functionality to extract data as tracked by the model

    def __init_functionality_extraction(self):
        """initialises a dictionary containing all possible functionality
        for extracting and formatting directly tracked data
        (that does not require additional calculations) in the model"""
        functionality = \
            {
                'time_x_agent':                                                                                         # data specific for individual time steps and individual agent
                    {
                        'general':
                            self.__extract_flat_agent_time_general,                                                     # Add generic data series always needed -> Iteration ID, Time ID, Agent ID, Agent Group ID
                        'forage_option_visit':
                            self.__extract_flat_agent_time_forage_option_visit,                                         # What Environment subsection / choice option / DiscreteAlternative did the agent forage in
                        'average_expected_competition':
                            self.__extract_flat_agent_time_average_expected_competition,                                # What is the theoretical amount of competitors an agent would encounter on the grid - MEASURE NOT RELIABLE
                        'realised_competition':
                            self.__extract_flat_agent_time_realised_competition,                                        # What is the actual amount of other agents and agent encountered while foraging
                        'knowledge_in_heatmap':
                            self.__extract_flat_agent_time_knowledge,                                                   # How many environment subsections / choice options / DiscreteAlternatives does agent have memory on
                        'heatmap_expectation':
                            self.__extract_flat_agent_time_heatmap_expectation,                                         # What did the agent expect he was going to catch while foraging in the chosen environmental subsection / choice option / DiscreteAlternative
                        'uncorrected_catch':
                            self.__extract_flat_agent_time_uncorrected_catch,                                           # What would and agent have caught in the chosen environmental subsection / choice option / DiscreteAlternative, if competition did not affect the catch
                        'realised_catch':
                            self.__extract_flat_agent_time_realised_catch                                               # What did an agent actually catch while foraging in a given time step
                        # INSERT FURTHER FUNCTIONALITY
                    },

                'time_x_environment':                                                                                   # data specific for individual time steps and individual environmental subsection / choice option / DiscreteAlternative
                    {
                        'id_agents_visited':
                            self.__extract_flat_environment_time_agents_visited,                                        # Which agents have visited an individual environmental subsection / choice option / DiscreteAlternative
                        'environmental_stock':
                            self.__extract_flat_environment_time_resource_stock,                                        # What is the stock in an individual environmental subsection / choice option / DiscreteAlternative
                        'nb_agents_visited':
                            self.__extract_flat_time_environment_time_nb_agents,                                        # how many agents have visited in an individual environmental subsection / choice option / DiscreteAlternative
                        'occurred_competition_correction':
                            self.__extract_flat_time_environment_competition_correction_occurred,                       # What was the correction for catch applied in an individual environmental subsection / choice option / DiscreteAlternative
                        'theoretical_competition_correction':
                            self.__extract_flat_time_environment_competition_correction_hypothetical,                   # What would have been the correction for catch applied in an individual environmental subsection / choice option / DiscreteAlternative, if one more agent chose to forage there
                        'agent_perceptions':
                            self.__extract_flat_environment_time_agent_perceptions,                                     # What did every agent (seperate data series for every agent) expect he was going to catch in  every environmental subsection / choice option / DiscreteAlternative
                        'agent_potential_real_catch':
                            self.__extract_flat_time_environment_agent_potential_catch                                  # What could an agent (seperate data series for every agent) have caught in an individual environmental subsection / choice option / DiscreteAlternative if it had foraged there without competition
                        # INSERT FURTHER FUNCTIONALITY
                    }

                # INSERT POTENTIAL OTHER OUTPUT DATA TYPES HERE
            }
        return functionality

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Extract Raw Agent by Time data --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def get_time_x_agent_data(self, agent_set, iteration_id, wanted_data='ALL'):
        """Method to extract data series that are specific for time and agents,
        desired outcome data can be defined as a list of names
        as a subset of the dictionary keys in the functionality dictionary,
        if 'wanted_data' is left emtpy all currently implemented data series are returned
        if wanted data is defined, it is recommended to include 'general' as id tags for all data series"""

        data_output = pd.DataFrame()                                                                                    # prepare output data container

        if wanted_data == 'ALL':
            for data_series_extractor in self.functionality_extraction['time_x_agent']:                                 # loop over all data series we have functionality on in the functionality dictionary and add each series to the pandas.Dataframe data container
                data_output = self.functionality_extraction['time_x_agent'][data_series_extractor](agent_set,
                                                                                                    data_output,
                                                                                                    iteration_id)
        elif isinstance(wanted_data, list):
            for data_series_extractor in wanted_data:
                if data_series_extractor not in self.functionality_extraction['time_x_agent']:                          # error handling: let user know wanted data series is not supported and print the data series that are supported)
                    raise NotImplementedError(
                        'defined data series {} is not supported as output data series,'.format(data_series_extractor) +
                        'supported functionalities are:\t{}'.format(
                            list(self.functionality_extraction['time_x_agent'].keys())))

                else:                                                                                                   # loop over all wanted data series and add each series to the pandas.Dataframe data container
                    data_output = self.functionality_extraction['time_x_agent'][data_series_extractor](agent_set,
                                                                                                   data_output,
                                                                                                   iteration_id)
        else:
            raise TypeError('Wanted data not specified properly, should be a list')                                     # error handling: when wanted data is not a list, rais error

        return data_output

    def __extract_flat_agent_time_general(self, agent_set, output_data=pd.DataFrame(), iteration_id=-99):
        """Extracts the ID columns for the data frame:
        iteration id, time step id, agent id, agent group id"""

        input_data = agent_set.agents                                                                                   # define what part of the agent fleet the data is at

        data_series_iteration = []                                                                                      # prepare data container for iteration id tags in the output data
        data_series_time = []                                                                                           # prepare data container for time id tags in the output data
        data_series_agent = []                                                                                          # prepare data container for agent id tags in the output data
        data_series_group_allegiance = []                                                                               # prepare data container for agent group id tags in the output data
        # data_series_catch = []

        for time_id in tuple(input_data[next(iter(input_data))].time_step_catch.keys()):                                # loop over the items (time_steps) in an immutable list of time_steps as logged in the time_step_catch tracker of the first agent in the model
            for agent in input_data:
                data_series_iteration.append(iteration_id)                                                              # fill data container for iteration id tags in the output data
                data_series_time.append(time_id)                                                                        # fill data container for time id tags in the output data
                data_series_agent.append(agent)                                                                         # fill data container for agent id tags in the output data
                data_series_group_allegiance.append(
                    input_data[agent].heatmap_exchanger.relevant_data['group_allegiance'])                              # fill data container for agent group id tags in the output data
                # data_series_catch.append(input_data[agent].time_step_catch[time_id])

        output_data['iteration_id'] = data_series_iteration                                                             # load data container for iteration id tags to match desired output data format
        output_data['time_id'] = data_series_time                                                                       # load data container for time id tags to match desired output data format
        output_data['agent_id'] = data_series_agent                                                                     # load data container for agent id tags to match desired output data format
        output_data['group_allegiance'] = data_series_group_allegiance                                                  # load data container for agent group id tags to match desired output data format
        # output_data['catch'] = data_series_catch
        # TODO: Catch as commented out above seems to be bugging, other tracker for catch yields other, more logical data -- DOUBLE Check functionality

        return output_data                                                                                              # return output data

    def __extract_flat_agent_time_forage_option_visit(self, agent_set, output_data=pd.DataFrame(), iteration=-99):
        """Extracts the Environment unit/Choice option/ DiscreteAlternative
        visited for every time step and agent"""

        input_data = agent_set.forage_visit_tracker                                                                     # define what part of the agent fleet the data is at

        data_series_forage_visits = []                                                                                  # prepare data container for the considered data series to load into the output data

        for time_id in tuple(input_data.keys()):                                                                        # fill data container for the considered data by looping over time and agents in the tracker variable
            for agent in input_data[time_id]:
                data_series_forage_visits.append(input_data[time_id][agent])                                            # add time and agent specific data point to prepared data container

        output_data['forage_visit'] = data_series_forage_visits                                                         # load data container into desired output data format

        return output_data                                                                                              # return output data

    def __extract_flat_agent_time_average_expected_competition(self, agent_set, output_data=pd.DataFrame(), iteration_id=-99):
        """Extracts the average expected competition for every time step and agent - Theoretical concept"""

        input_data = agent_set.average_expected_competitor_tracker                                                      # define what part of the agent fleet the data is at

        data_series_competition = []                                                                                    # prepare data container for the considered data series to load into the output data

        for time_id in tuple(input_data.keys()):                                                                        # fill data container for the considered data by looping over time and agents in the tracker variable
            for agent in input_data[time_id]:
                data_series_competition.append(input_data[time_id][agent])                                              # add time and agent specific data point to prepared data container

        output_data['average_expected_competitors'] = data_series_competition                                           # load data container into desired output data format

        return output_data                                                                                              # return output data

    def __extract_flat_agent_time_realised_competition(self, agent_set, output_data=pd.DataFrame(), iteration_id=99):
        """Extract the competition encountered (as number other agents foraging in the same choice)
         by every individual agent for every time step"""

        input_data = agent_set.realised_competition_tracker                                                             # define what part of the agent fleet the data is at

        data_series_realised_competition = []                                                                           # prepare data container for the considered data series to load into the output data

        for time_id in tuple(input_data.keys()):                                                                        # fill data container for the considered data by looping over time and agents in the tracker variables
            for agent in input_data[time_id]:
                data_series_realised_competition.append(input_data[time_id][agent])                                     # add time and agent specific data point to prepared data container

        output_data['realised_competition'] = data_series_realised_competition                                          # load data container into desired output data format

        return output_data                                                                                              # return output data

    def __extract_flat_agent_time_knowledge(self, agent_set, output_data=pd.DataFrame(), iteration_id=-99):
        """Extracts the heatmap fill (as number of choice options with a memory entry)
         for every time step and agent"""

        input_data = agent_set.agents                                                                                   # define what part of the agent fleet the data is at

        data_series_knowledge = []                                                                                      # prepare data container for the considered data series to load into the output data

        for time_id in tuple(input_data[next(iter(input_data))].knowledge_evolution_tracker.keys()):                    # fill data container for the considered data by looping over time and agents in the tracker variables
            for agent in input_data:
                data_series_knowledge.append(len(input_data[agent].knowledge_evolution_tracker[time_id]))               # add time and agent specific data point to prepared data container

        output_data['knowledge_in_heatmap'] = data_series_knowledge                                                     # load data container into desired output data format

        return output_data                                                                                              # return output data

    def __extract_flat_agent_time_heatmap_expectation(self, agent_set, output_data=pd.DataFrame(), iteration_id=99):
        """Extracts the expected amount of catch (as entry in an agent's heatmap entry for the chosen choice options)
         for every time step and agent"""

        input_data = agent_set.heatmap_expectation_tracker                                                              # define what part of the agent fleet the data is at

        data_series_heatmap_expectation = []                                                                            # prepare data container for the considered data series to load into the output data

        for time_id in tuple(input_data.keys()):                                                                        # fill data container for the considered data by looping over time and agents in the tracker variables
            for agent in input_data[time_id]:
                data_series_heatmap_expectation.append(input_data[time_id][agent])                                      # add time and agent specific data point to prepared data container

        output_data['heatmap_expected_catch'] = data_series_heatmap_expectation                                         # load data container into desired output data format

        return output_data                                                                                              # return output data

    def __extract_flat_agent_time_uncorrected_catch(self, agent_set, output_data=pd.DataFrame(), iteration_id=99):
        """Extracts the theoretical catch that would have been achieved in the absence of competition,
         for every time step and agent"""

        input_data = agent_set.uncorrected_catch_tracker                                                                # define what part of the agent fleet the data is at

        data_series_uncorrected_catch = []                                                                              # prepare data container for the considered data series to load into the output data

        for time_id in tuple(input_data.keys()):                                                                        # fill data container for the considered data by looping over time and agents in the tracker variables
            for agent in input_data[time_id]:
                data_series_uncorrected_catch.append(input_data[time_id][agent])                                        # add time and agent specific data point to prepared data container

        output_data['uncorrected_catch'] = data_series_uncorrected_catch                                                # load data container into desired output data format

        return output_data                                                                                              # return output data

    def __extract_flat_agent_time_realised_catch(self, agent_set, output_data=pd.DataFrame(), iteration_id=99):
        """Extracts the realised catch that is achieved
         for every time step and agent"""

        input_data = agent_set.corrected_catch_tracker                                                                  # define what part of the agent fleet the data is at

        data_series_realised_catch = []                                                                                 # prepare data container for the considered data series to load into the output data

        for time_id in tuple(input_data.keys()):                                                                        # fill data container for the considered data by looping over time and agents in the tracker variables
            for agent in input_data[time_id]:
                data_series_realised_catch.append(input_data[time_id][agent])                                           # add time and agent specific data point to prepared data container

        output_data['realised_catch'] = data_series_realised_catch                                                      # load data container into desired output data format

        return output_data                                                                                              # return output data

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Extract Raw Environment/Choice Set by Time data ------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def get_time_x_environment_data(self, agent_set, choice_set, iteration_id):
        """Extract unaggregated time by individual choice option/ environment subsection data
        for all implemented functionality"""

        input_data = choice_set.stock_time_tracker                                                                      # define what part of the choice set/environment object the data is at

        data_output = pd.DataFrame()                                                                                    # prepare output data container

        # get basic information data series (iteration data series, time series and alternative ID series)
        data_series_iteration = []                                                                                      # prepare data container for iteration id tag data series to load into the output data container
        data_series_time = []                                                                                           # prepare data container for time id tag data series to load into the output data
        data_series_alternatives = []                                                                                   # prepare data container for choice_option/environment subsection tag data series to load into the output data

        for time_id in input_data:                                                                                      # fill data container for the considered data by looping over time and choice options in the tracker variables
            for alternative in choice_set.discrete_alternatives:
                data_series_iteration.append(iteration_id)                                                              # fill data container for iteration id tags in the output data
                data_series_time.append(time_id)                                                                        # fill data container for time id tags in the output data
                data_series_alternatives.append(alternative)                                                            # fill data container for choice option/ environment subsection id tags in the output data

        data_output['iteration_id'] = data_series_iteration                                                             # load iteration id tag data container into desired output data format
        data_output['time_id'] = data_series_time                                                                       # load time id tag data container into desired output data format
        data_output['alternative_id'] = data_series_alternatives                                                        # load choice option tag data container into desired output data format

        # include iteration ID, time_id and alternative ID
        for data_series_extractor in self.functionality_extraction['time_x_environment']:                               # loop over all data series we have functionality on in the functionality dictionary and add each series to the pandas.Dataframe data container

            data_output = \
                self.functionality_extraction['time_x_environment'][data_series_extractor](agent_set=agent_set,
                                                                                           choice_set=choice_set,
                                                                                           data_output=data_output,
                                                                                           iteration_id=iteration_id)
        return data_output                                                                                              # return output data

    def __extract_flat_environment_time_agents_visited(self, agent_set, choice_set, data_output, iteration_id):

        input_data = agent_set.forage_visit_tracker                                                                     # define what part of the agent fleet the data is at

        data_series_agents_visited = []                                                                                 # prepare data container for the considered data series to load into the output data

        for time_id in input_data:
            for alternative in choice_set.discrete_alternatives:                                                        # fill data container for the considered data by looping over time and choice options in the tracker variables
                agents_visited = '|'.join([key for key, value in input_data[time_id].items() if value == alternative])  # construct data point using list comprehension (find what agents (keys) have chosen the considered choice_option/DiscretAlternative/Environment Unit (values)
                data_series_agents_visited.append(agents_visited)                                                       # add time and choice option specific data point to prepared data container

        data_output['agents_visited'] = data_series_agents_visited                                                      # load data container into desired output data format

        return data_output                                                                                              # return output data

    def __extract_flat_environment_time_resource_stock(self, agent_set, choice_set, data_output, iteration_id):
        """Extracts the resource stock that is present
         for every time step and individual Choice Option/Environment Unit/ DiscreteAlternative"""

        input_data = choice_set.stock_time_tracker                                                                      # define what part of the choice set/environment object the data is at

        data_series_stock = []                                                                                          # prepare data container for the considered data series to load into the output data

        for time_id in input_data:                                                                                      # fill data container for the considered data by looping over time and choice options in the tracker variables
            for alternative in input_data[time_id]:
                data_series_stock.append(input_data[time_id][alternative])                                              # add time and choice option specific data point to prepared data container

        data_output['real_stock'] = data_series_stock                                                                   # load data container into desired output data format

        return data_output                                                                                              # return output data

    def __extract_flat_time_environment_time_nb_agents(self, agent_set, choice_set, data_output, iteration_id):
        """Extracts the number of agents that has visited
         for every time step and individual Choice Option/Environment Unit/ DiscreteAlternative"""

        input_data = choice_set.time_visit_map                                                                          # define what part of the choice set/environment object the data is at

        data_series_nb_agents = []                                                                                      # prepare data container for the considered data series to load into the output data

        for time_id in input_data[next(iter(input_data))]:
            for alternative in input_data:
                data_series_nb_agents.append(input_data[alternative][time_id])

        data_output['nb_agents_visited'] = data_series_nb_agents                                                        # load data container into desired output data format

        return data_output                                                                                              # return output data

    def __extract_flat_time_environment_competition_correction_occurred(self, agent_set, choice_set, data_output,
                                                                        iteration_id):
        """Extracts the correction factor that was used to correct catch for any forager having foraged
        for every time step and any given individual Choice Option/Environment Unit/ DiscreteAlternative """
        input_data = choice_set.competition_correction                                                                  # define what part of the choice set/environment object the data is at

        data_series_competition_correction = []                                                                         # prepare data container for the considered data series to load into the output data

        for time_id in input_data:                                                                                      # fill data container for the considered data by looping over time and choice options in the tracker variables
            for alternative in input_data[time_id]:
                data_series_competition_correction.append(input_data[time_id][alternative])                             # add time and choice option specific data point to prepared data container

        data_output['occurred_competition_correction'] = data_series_competition_correction                             # load data container into desired output data format

        return data_output                                                                                              # return output data

    def __extract_flat_time_environment_competition_correction_hypothetical(self, agent_set, choice_set, data_output,
                                                                            iteration_id):
        """Extracts the theoretical correction factor that would have been used to correct catch for any forager foraging
        if the number of agents foraging in any given  Choice Option/Environment Unit/ DiscreteAlternative was increased
        by one,
        for every time step and any given individual Choice Option/Environment Unit/ DiscreteAlternative """
        input_data = choice_set.hypothetical_competition_correction                                                     # define what part of the choice set/environment object the data is at

        data_series_hypothetical_competition_correction = []                                                            # prepare data container for the considered data series to load into the output data

        for time_id in input_data:                                                                                      # fill data container for the considered data by looping over time and choice options in the tracker variables
            for alternative in input_data[time_id]:
                data_series_hypothetical_competition_correction.append(input_data[time_id][alternative])                # add time and choice option specific data point to prepared data container

        data_output['hypothetical_competition_correction'] = data_series_hypothetical_competition_correction            # load data container into desired output data format

        return data_output                                                                                              # return output data

    # TODO: potential issue with 'perceptions' in nomenclature, is used in stock assessment terminology on a regular basis for other variables
    def __extract_flat_environment_time_agent_perceptions(self, agent_set, choice_set, data_output, iteration_id):
        """Extracts the catch for every agent (separate data series/column) expects to achieve when fishing,
         for every time step and individual Choice Option/Environment Unit/ DiscreteAlternative"""

        input_data = agent_set.heatmap_tracker                                                                          # define what part of the agent fleet the data is at

        for agent in agent_set.agents:                                                                                  # loop over every agent to get a seperate data series for every individual agent
            agent_expected_catch_series = []                                                                            # prepare data container for the considered data series to load into the output data
            for time in input_data:                                                                                     # fill data container for the considered data by looping over time and choice options in the tracker variables
                for alternative in input_data[time][agent]:
                    agent_expected_catch_series.append(input_data[time][agent][alternative])                            # add time and choice option specific data point to prepared data container

            data_output[agent + '_catch_expectation_heatmap'] = agent_expected_catch_series                             # load data container (for a specific agent) into desired output data format

        return data_output                                                                                              # return output data

    def __extract_flat_time_environment_agent_potential_catch(self, agent_set, choice_set, data_output, iteration_id):
        """Extracts the catch that every agent (separate data series/column) could have achieved when fishing
        (not taking into account competition),
        for every time step and individual Choice Option/Environment Unit/ DiscreteAlternative"""

        input_data = agent_set.catch_potential_tracker                                                                  # define what part of the agent fleet the data is at

        for agent in agent_set.agents:                                                                                  # loop over every agent to get a seperate data series for every individual agent
            agent_catch_potential_series = []                                                                           # prepare data container for the considered data series to load into the output data
            for time in input_data:                                                                                     # fill data container for the considered data by looping over time and choice options in the tracker variables
                for alternative in input_data[time][agent]:
                    agent_catch_potential_series.append(input_data[time][agent][alternative])                           # add time and choice option specific data point to prepared data container

            data_output[agent + '_catch_potential'] = agent_catch_potential_series                                      # load data container (for a specific agent) into desired output data format
            # TODO: Quick and dirty fix does not take competition into account
        return data_output                                                                                              # return output data

# ----------------------------------------------------------------------------------------------------------------------
# ---------------- Junk/ Remnant methods that need to be checked if still usable/necessary/salvageable -----------------
# ----------------------------------------------------------------------------------------------------------------------

    # TODO: relic method: Check if still needed
    def extract_average_expected_competition(self, agent_set):
        """extract data series on Theoretical expected competition over time for every agent"""

        data_output = pd.DataFrame(agent_set.average_expected_competitor_tracker).transpose()                           # make a pd.Dataframe from the data on the average number of competitors in a given choice option
        data_output.insert(loc=0, column='time_step_id', value=data_output.index)                                       # repair small error in tracker->pd.dataframe conversion --> get time_step column from index
        data_output.reset_index(inplace=True)                                                                           # reset index values to default indices
        data_output.drop(columns='index', inplace=True)                                                                 # remove newly created redundant column 'index'

        return data_output

    # TODO: Move to module derive_statistics to keep raw data extraction and derived data separate
    def extract_time_x_group_catch(self, dataframe):
        """QUICK AND DIRTY WAY TO GET GROUP SPECIFIC CATCH OVER TIME FOR A SINGLE SIMULATION"""                         # TODO: Check if still quick and dirty

        data_dictionary = defaultdict(list)

        unique_values_time = dataframe['time_id'].unique()
        unique_values_group = dataframe['group_allegiance'].unique()

        for time_id in unique_values_time:
            time_temp_df = dataframe[dataframe.time_id == time_id]
            data_dictionary['time_id'].append(time_id)
            for group in unique_values_group:
                temp_group_df = time_temp_df[dataframe.group_allegiance == group]
                data_dictionary[group].append(temp_group_df['corrected_catch'].sum())

        output_dataframe = pd.DataFrame(data_dictionary)

        return output_dataframe
