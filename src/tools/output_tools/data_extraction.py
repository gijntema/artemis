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

this module is read by ARTEMIS.py to transform the model output into usable (raw) data formats: pandas.Dataframe objects

Module inputs:
-   No Modules
-   Module only works on objects defined in the modules agents.py and choice_set.py

Module Usage:
-   methods of the DataTransformer object are used in ARTEMIS.py

Last Updated:
    06-09-2021

Version Number:
    0.1
"""

# import external packages
import pandas as pd


# TODO: --FUNCTIONALITY-- add desired functionality, only some examples of data are implemented for now:
# - Total Forage Effort per Alternative (check)
# - Final Resource Stock per Alternative
# - Total Catch per Agent
# - time_step total industry/population catch

# TODO:  --STRUCTURAL -- make flexible to choose desired reporter measures more easily
#  (e.g. make a library dictionary to call on)

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------ Main Functionality Method -------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class DataTransformer:
    """" Restructures the data outputs from the model to a usable data format (a pandas.Dataframe object)"""

    def transform_output_data(self, choice_set, agent_set, duration, iteration_id=1):
        """main functionality method, extracts data (currently hardcoded) from agents and choice options,
        producing pandas.Dataframe objects"""
        alternative_specific_data = self.__transform_alternative_data(choice_set, iteration_id)
        choice_set_time_series = self.__transform_alternative_time_series_data(choice_set, duration, iteration_id)
        agent_specific_data = self.__transform_agent_data(agent_set, iteration_id)
        agent_set_time_series = self.__transform_agent_time_series_data(agent_set, duration, iteration_id)

        return alternative_specific_data, choice_set_time_series, agent_specific_data, agent_set_time_series
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------ Primary Subsections of the Main Functionality Method ----------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __transform_alternative_data(self, choice_set, iteration_id=99):
        # extract list of alternatives
        temp_dictionary = dict()
        temp_dictionary['alternative_id'] = self.__extract_list_of_alternatives(choice_set)

        # currently implemented extractable data
        temp_dictionary['alternative_effort'] = self.__transform_alternative_effort_data(choice_set)
        temp_dictionary['alternative_final_stock'] = self.__transform_final_stock_data(choice_set)
        # add additional functionality HERE

        # change to DataFrame format
        alternative_data = pd.DataFrame(temp_dictionary)

        # add iteration_id to dataframe
        iteration_id = ['iteration_' + str(iteration_id)] * len(temp_dictionary['alternative_id'])
        alternative_data.insert(0, 'iteration_id', iteration_id)

        return alternative_data

    def __transform_alternative_time_series_data(self, choice_set, duration, iteration_id=99):
        # extract list of time_steps
        temp_dictionary = {}
        temp_dictionary['time_step_id'] = self.__extract_list_of_time_steps(duration)

        # currently implemented extractable data TODO: --FUNCTIONALITY-- implement examples for time_step alternative data
        # add additional functionality HERE
        # CONSIDERING TIME_STEP EFFORT GINI COEFFICIENT AS MEASURE FOR EQUALITY IN ENVIRONMENTAL PRESSURE

        # change to DataFrame format
        alternative_time_series_data = pd.DataFrame(temp_dictionary)

        # add iteration_id to dataframe
        iteration_id = ['iteration_' + str(iteration_id)] * len(temp_dictionary['time_step_id'])
        alternative_time_series_data.insert(0, 'iteration_id', iteration_id)

        return alternative_time_series_data

    def __transform_agent_data(self, agent_set, iteration_id=-99):
        # extract list of time_steps
        temp_dictionary = dict()
        temp_dictionary['agent_id'] = self.__extract_list_of_agents(agent_set)

        # currently implemented extractable data
        temp_dictionary['agents_catch'] = self.__transform_agent_catch_data(agent_set)
        # add additional functionality HERE


        # change to DataFrame format
        alternative_time_series_data = pd.DataFrame(temp_dictionary)

        # add iteration_id to dataframe
        iteration_id = ['iteration_' + str(iteration_id)] * len(temp_dictionary['agent_id'])
        alternative_time_series_data.insert(0, 'iteration_id', iteration_id)

        return alternative_time_series_data

    def __transform_agent_time_series_data(self, agent_set, duration, iteration_id=99):
        # TODO: --STRUCTURAL-- near-duplicate of method transform_alternative_time_series_data, could be merged?
        # extract list of time_steps
        temp_dictionary = dict()
        temp_dictionary['time_step_id'] = self.__extract_list_of_time_steps(duration)

        # currently implemented extractable data
        temp_dictionary['total_catch'] = self.__transform_agent_set_total_catch_data(agent_set)
        # add additional functionality HERE
        # CONSIDERING TIME_STEP CATCH GINI COEFFICIENT AS MEASURE FOR EQUALITY IN AGENT INCOME

        # change to DataFrame format
        agent_time_series_data = pd.DataFrame(temp_dictionary)

        # add iteration_id to dataframe
        iteration_id = ['iteration_' + str(iteration_id)] * len(temp_dictionary['time_step_id'])
        agent_time_series_data.insert(0, 'iteration_id', iteration_id)

        return agent_time_series_data

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Internal Methods to Extract Label Data Series --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __extract_list_of_time_steps(self, duration_model):
        time_steps = list()
        duration_counter = 0
        while duration_counter < duration_model:
            time_steps.append(str(duration_counter))
            duration_counter += 1

        return time_steps

    def __extract_list_of_alternatives(self, choice_set):
        alternatives = list(choice_set.discrete_alternatives.keys())
        alternative_counter = 0
        while alternative_counter < len(alternatives):
            alternatives[alternative_counter] = alternatives[alternative_counter].split("_")[1]
            alternative_counter += 1

        return alternatives

    def __extract_list_of_agents(self, agent_set):
        agents = list(agent_set.agents.keys())
        agent_counter = 0
        while agent_counter < len(agents):
            agents[agent_counter] = agents[agent_counter].split("_")[1]
            agent_counter += 1

        return agents
# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Internal Methods to Extract Actual Data Series -------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __transform_alternative_effort_data(self, choice_set):

        effort_data = list(choice_set.effort_map.values())

        return effort_data

    def __transform_agent_catch_data(self, agent_set):
        catch_data = agent_set.agents

        # extract list of values for each agent
        catch = list()
        for agent in catch_data:
            catch.append(catch_data[agent].total_catch)

        return catch

    def __transform_agent_set_total_catch_data(self, agent_set):

        # extract list of values for every time_step
        time_step_catch = list(agent_set.total_time_step_catch_tracker.values())

        return time_step_catch

    def __transform_final_stock_data(self, choice_set):
        final_stock_data = choice_set.discrete_alternatives

        final_stock = []
        for alternative in final_stock_data:
            final_stock.append(final_stock_data[alternative].resource_stock)

        return final_stock


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Methods to Extract Data Related to Distributional Effects --------------------------
# ----------------------------------------------------------------------------------------------------------------------


    def __extract_time_step_catch_data(self, agent_set, time_step):
        catch_list = []
        data = agent_set.agents
        for agent in data:
            catch_list.append(data[agent].time_steps_catch[time_step])

        return catch_list

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Methods to Extract Average Data Series ---------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def get_average_dataframes(self, alternative_specific_data, alternative_time_series_data,
                               agent_specific_data, agent_time_series_data):

        avg_alternative_specific = self.__get_average_alternative_specific(alternative_specific_data)
        avg_alternative_time = self.__get_average_alternative_time_series(alternative_time_series_data)
        avg_agent_specific = self.__get_average_agent_specific(agent_specific_data)
        avg_agent_time = self.__get_average_agent_time_series(agent_time_series_data)

        return avg_alternative_specific, avg_alternative_time, avg_agent_specific, avg_agent_time

    def __get_average_alternative_specific(self, alternative_specific_data):
        temp_data = alternative_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('alternative_id').mean()
        temp_data['alternative_id'] = temp_data.index

        return temp_data

    def __get_average_alternative_time_series(self, alternative_time_series_data):
        temp_data = alternative_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').mean()
        temp_data['time_step_id'] = temp_data.index

        return temp_data

    def __get_average_agent_specific(self, agent_specific_data):
        temp_data = agent_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('agent_id').mean()
        temp_data['agent_id'] = temp_data.index

        return temp_data

    def __get_average_agent_time_series(self, agent_time_series_data):
        temp_data = agent_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').mean()
        temp_data['time_step_id'] = temp_data.index

        return temp_data
