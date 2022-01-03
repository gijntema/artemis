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
-   methods of the DataTransformer object are used in ARTEMIS.py,
    outputs generated there are then used as input for export_data.py and outcome_visualization.py

Last Updated:
    01-10-2021

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
        """make a functionality dictionary,
        only for future functionality/flexibility,
        aids runtime and readability"""

        self.functionality_extraction = self.__init_functionality_extraction()                                          # functionality to extract data as tracked by the model

    def __init_functionality_extraction(self):  # PLACE HOLDER FOR future reworking of the structure
        """intialises a dictionary containing all possible functionality
        for extracting and formatting directly tracked data in the model"""
        functionality = \
            {
                'time_x_agent':
                    {
                        'catch': self.__extract_flat_agent_time_catch,
                        'forage_option_visit': self.__extract_flat_agent_time_forage_option_visit,
                        'competition': self.__extract_flat_agent_time_competition,
                        'realised_competition': self.__extract_flat_agent_time_realised_competition,
                        'knowledge_in_heatmap': self.__extract_flat_agent_time_knowledge,
                        'heatmap_expectation': self.__extract_flat_agent_time_heatmap_expectation,
                        'uncorrected_catch': self.__extract_flat_agent_time_uncorrected_catch,
                        'corrected_catch': self.__extract_flat_agent_time_corrected_catch
                        # INSERT FURTHER FUNCTIONALITY
                    },
                'time_x_environment':
                    {
                        'environmental_stock': self.__extract_flat_environment_time_resource_stock,
                        'agent_perceptions': self.__extract_flat_environment_time_agent_perceptions
                        # INSERT FURTHER FUNCTIONALITY
                    }

                # INSERT POTENTIAL OTHER DATA TYPES HERE
            }
        return functionality

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Extract Raw Agent by Time data --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def get_time_x_agent_data(self, agent_set, iteration_id):
        """Extract unaggregated agent by time data for all implemented functionality"""
        data_output = pd.DataFrame()
        for data_series_extractor in self.functionality_extraction['time_x_agent']:                                     # loop over all data series, as potential explanatory variables to catch, we have functionality on in the functionality dictionary (quick and dirty fix, could be adapted to choose specific functionality)
            data_output = self.functionality_extraction['time_x_agent'][data_series_extractor](agent_set,
                                                                                                data_output,
                                                                                                iteration_id)
        return data_output

    def extract_average_expected_competition(self, agent_set):
        """Theoretical expected competition over time for every agent"""
        data_output = pd.DataFrame(agent_set.average_expected_competitor_tracker).transpose()                           # make a pd.Dataframe from the data on the average number of competitors in a given choice option
        data_output.insert(loc=0, column='time_step_id', value=data_output.index)                                       # repair small error in tracker->pd.dataframe conversion --> get time_step column from index
        data_output.reset_index(inplace=True)                                                                           # reset index values to default indices
        data_output.drop(columns='index', inplace=True)                                                                 # remove newly created redundant column 'index'
        return data_output

    def __extract_flat_agent_time_catch(self, agent_set, output_data=pd.DataFrame(), iteration_id=-99):
        """Extracts the ID columns for the data frame: iterations, time step, agent ID  and catch"""
        input_data = agent_set.agents
        data_series_iteration = []
        data_series_time = []
        data_series_agent = []
        data_series_group_allegiance = []
        data_series_catch = []

        for time_id in tuple(input_data[next(iter(input_data))].time_step_catch.keys()):                                # loop over the items (time_steps) in an immutable list of time_steps as logged in the time_step_catch tracker of the first agent in the model
            for agent in input_data:
                data_series_iteration.append(iteration_id)
                data_series_time.append(time_id)
                data_series_agent.append(agent)
                data_series_group_allegiance.append(input_data[agent].heatmap_exchanger.relevant_data['group_allegiance'])
                data_series_catch.append(input_data[agent].time_step_catch[time_id])

        output_data['iteration_id'] = data_series_iteration
        output_data['time_id'] = data_series_time
        output_data['agent_id'] = data_series_agent
        output_data['group_allegiance'] = data_series_group_allegiance
        output_data['catch'] = data_series_catch                                                                        # TODO: Migrate to other function
        # TODO Move 'Catch' to separate method

        return output_data

    def __extract_flat_agent_time_competition(self, agent_set, output_data=pd.DataFrame(), iteration_id=-99):
        """Extracts the average expected competition for every time step and agent"""
        data_series_competition = []
        input_data = agent_set.average_expected_competitor_tracker
        for time_id in tuple(input_data.keys()):
            for agent in input_data[time_id]:
                data_series_competition.append(input_data[time_id][agent])

        output_data['average_expected_competitors'] = data_series_competition

        return output_data

    def __extract_flat_agent_time_knowledge(self, agent_set, output_data=pd.DataFrame(), iteration_id=-99):
        """Extracts the heatmap fill for every time step and agent"""
        data_series_knowledge = []
        input_data = agent_set.agents
        for time_id in tuple(input_data[next(iter(input_data))].knowledge_evolution_tracker.keys()):
            for agent in input_data:
                data_series_knowledge.append(len(input_data[agent].knowledge_evolution_tracker[time_id]))

        output_data['knowledge_in_heatmap'] = data_series_knowledge
        return output_data

    def __extract_flat_agent_time_forage_option_visit(self, agent_set, output_data=pd.DataFrame(), iteration=-99):
        data_series_forage_visits = []
        """Extracts the Choice option visited for every time step and agent"""
        input_data = agent_set.forage_visit_tracker
        for time_id in tuple(input_data.keys()):
            for agent in input_data[time_id]:
                data_series_forage_visits.append(input_data[time_id][agent])
        output_data['forage_visit'] = data_series_forage_visits
        return output_data

    def __extract_flat_agent_time_heatmap_expectation(self, agent_set, output_data=pd.DataFrame(), iteration_id=99):
        input_data = agent_set.heatmap_expectation_tracker
        data_series_heatmap_expectation = []
        for time_id in tuple(input_data.keys()):
            for agent in input_data[time_id]:
                data_series_heatmap_expectation.append(input_data[time_id][agent])
        output_data['heatmap_expected_catch'] = data_series_heatmap_expectation
        return output_data

    def __extract_flat_agent_time_uncorrected_catch(self, agent_set, output_data=pd.DataFrame(), iteration_id=99):
        input_data = agent_set.uncorrected_catch_tracker
        data_series_uncorrected_catch = []
        for time_id in tuple(input_data.keys()):
            for agent in input_data[time_id]:
                data_series_uncorrected_catch.append(input_data[time_id][agent])
        output_data['uncorrected_catch'] = data_series_uncorrected_catch
        return output_data

    def __extract_flat_agent_time_realised_competition(self, agent_set, output_data=pd.DataFrame(), iteration_id=99):
        input_data = agent_set.realised_competition_tracker
        data_series_realised_competition = []
        for time_id in tuple(input_data.keys()):
            for agent in input_data[time_id]:
                data_series_realised_competition.append(input_data[time_id][agent])
        output_data['realised_competition'] = data_series_realised_competition
        return output_data

    def __extract_flat_agent_time_corrected_catch(self, agent_set, output_data=pd.DataFrame(), iteration_id=99):
        input_data = agent_set.corrected_catch_tracker
        data_series_corrected_catch = []
        for time_id in tuple(input_data.keys()):
            for agent in input_data[time_id]:
                data_series_corrected_catch.append(input_data[time_id][agent])
        output_data['corrected_catch'] = data_series_corrected_catch
        return output_data

    # TODO: Decide what to do with this method, Do we still need it or this more for a data transformer module, rather then a data extractor module?
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
                data_dictionary[group].append(temp_group_df['catch'].sum())

        output_dataframe = pd.DataFrame(data_dictionary)
        return output_dataframe

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Extract Raw Environment/Choice Set by Time data ------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def get_time_x_environment_data(self, agent_set, choice_set, iteration_id):
        """Extract unaggregated environment by time data for all implemented functionality"""
        input_data = choice_set.stock_time_tracker
        data_output = pd.DataFrame()

        # get basic information data series (iteration data series, time series and alternative ID series)
        data_series_iteration = []
        data_series_time = []
        data_series_alternatives = []
        for time_id in input_data:
            for alternative in choice_set.discrete_alternatives:
                data_series_iteration.append(iteration_id)
                data_series_time.append(time_id)
                data_series_alternatives.append(alternative)

        data_output['iteration_id'] = data_series_iteration
        data_output['time_id'] = data_series_time
        data_output['alternative_id'] = data_series_alternatives

        # include iteration ID, time_id and alternative ID
        for data_series_extractor in self.functionality_extraction['time_x_environment']:                                     # loop over all data series, as potential explanatory variables to catch, we have functionality on in the functionality dictionary (quick and dirty fix, could be adapted to choose specific functionality)

            data_output = \
                self.functionality_extraction['time_x_environment'][data_series_extractor](agent_set=agent_set,
                                                                                           choice_set=choice_set,
                                                                                           data_output=data_output,
                                                                                           iteration_id=iteration_id)
        return data_output

    def __extract_flat_environment_time_resource_stock(self, agent_set, choice_set, data_output, iteration_id):
        input_data = choice_set.stock_time_tracker
        data_series_stock = []
        for time_id in input_data:
            for alternative in input_data[time_id]:
                data_series_stock.append(input_data[time_id][alternative])

        data_output['real_stock'] = data_series_stock
        return data_output

    def __extract_flat_environment_time_agent_perceptions(self, agent_set, choice_set, data_output, iteration_id):
        input_data = agent_set.heatmap_tracker
        for agent in agent_set.agents:
            agent_expected_catch_series = []
            for time in input_data:
                for alternative in input_data[time][agent]:
                    agent_expected_catch_series.append(input_data[time][agent][alternative])
            data_output[agent + '_catch_expectation_heatmap'] = agent_expected_catch_series

        return data_output

# EOF