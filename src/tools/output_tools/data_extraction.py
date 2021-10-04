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
# TODO: likely some duplicate functions present, future check should identify what is done twice


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
    def __init__(self):
        """make a functionality dictionary,
        only for future functionality/flexibility,
        not implemented in current version"""

        self.functionality = \
            {
                'avg': self.get_average_dataframes,
                'sd': self.get_sd_dataframes
            }

    def transform_output_data(self, choice_set, agent_set, duration, iteration_id=1):
        """main functionality method, extracts data (currently hardcoded) from agents and choice options,
        producing pandas.Dataframe objects for a single iteration/simulation"""
        alternative_specific_data = self.__transform_alternative_data(choice_set, iteration_id)
        choice_set_time_series = self.__transform_alternative_time_series_data(choice_set, duration, iteration_id)
        agent_specific_data = self.__transform_agent_data(agent_set, iteration_id)
        agent_set_time_series = self.__transform_agent_time_series_data(agent_set, duration, iteration_id)

        return alternative_specific_data, choice_set_time_series, agent_specific_data, agent_set_time_series

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------ Primary Subsections of the transform_output_data Method -------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __transform_alternative_data(self, choice_set, iteration_id=99):
        """ Method to extract data related to specific choice options to a usable format"""
        temp_dictionary = dict()
        temp_dictionary['alternative_id'] = self.__extract_list_of_alternatives(choice_set)                             # attach choice option IDs as independent variables

        # currently implemented extractable data
        temp_dictionary['alternative_effort'] = self.__transform_alternative_effort_data(choice_set)                    # add response variable total effort exerted by agents over all time steps given to each specific choice option
        temp_dictionary['alternative_final_stock'] = self.__transform_final_stock_data(choice_set)                      # add data of final resource stock at the end of a simulation (as diagnostic data) for each choice option specific
        # add additional functionality HERE

        # change to DataFrame format
        alternative_data = pd.DataFrame(temp_dictionary)

        # add iteration_id to dataframe
        iteration_id = ['iteration_' + str(iteration_id)] * len(temp_dictionary['alternative_id'])                      # add a tag for the iteration an a data point originates from to each data point
        alternative_data.insert(0, 'iteration_id', iteration_id)                                                        # insert itertaion ID as first column in the new data format

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
        """"function to retrieve data per time step for each agent and transform to usable format"""
        # extract list of time_steps
        temp_dictionary = dict()
        temp_dictionary['agent_id'] = self.__extract_list_of_agents(agent_set)

        # currently implemented extractable data
        temp_dictionary['agents_catch'] = self.__transform_agent_catch_data(agent_set)                                  # get agent specific total catch data (over all iteration time_steps) for each specific agent
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
            time_id = str(duration_counter).zfill(len(str(duration_model)))
            time_steps.append(time_id)
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

# TODO: quick and dirty fix for some basic measures, needs better flexibility through functionality dictionary
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

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------- Methods to Extract standard deviation Data Series ----------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def get_sd_dataframes(self, alternative_specific_data, alternative_time_series_data,
                               agent_specific_data, agent_time_series_data):

        sd_alternative_specific = self.__get_sd_alternative_specific(alternative_specific_data)
        sd_alternative_time = self.__get_sd_alternative_time_series(alternative_time_series_data)
        sd_agent_specific = self.__get_sd_agent_specific(agent_specific_data)
        sd_agent_time = self.__get_sd_agent_time_series(agent_time_series_data)

        return sd_alternative_specific, sd_alternative_time, sd_agent_specific, sd_agent_time

    def __get_sd_alternative_specific(self, alternative_specific_data):
        temp_data = alternative_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('alternative_id').std()
        temp_data['alternative_id'] = temp_data.index

        return temp_data

    def __get_sd_alternative_time_series(self, alternative_time_series_data):
        temp_data = alternative_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').std()
        temp_data['time_step_id'] = temp_data.index

        return temp_data

    def __get_sd_agent_specific(self, agent_specific_data):
        temp_data = agent_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('agent_id').std()
        temp_data['agent_id'] = temp_data.index

        return temp_data

    def __get_sd_agent_time_series(self, agent_time_series_data):
        temp_data = agent_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').std()
        temp_data['time_step_id'] = temp_data.index

        return temp_data


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------- Methods to Extract Quantile values for Data Series -----------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def get_qt_dataframes(self, alternative_specific_data, alternative_time_series_data,
                          agent_specific_data, agent_time_series_data, quantile=0.95):

        qt_alternative_specific = self.__get_qt_alternative_specific(alternative_specific_data, quantile)
        qt_alternative_time = self.__get_qt_alternative_time_series(alternative_time_series_data, quantile)
        qt_agent_specific = self.__get_qt_agent_specific(agent_specific_data, quantile)
        qt_agent_time = self.__get_qt_agent_time_series(agent_time_series_data, quantile)

        return qt_alternative_specific, qt_alternative_time, qt_agent_specific, qt_agent_time

    def __get_qt_alternative_specific(self, alternative_specific_data, quantile):
        temp_data = alternative_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('alternative_id').quantile(q=quantile)
        temp_data['alternative_id'] = temp_data.index

        return temp_data

    def __get_qt_alternative_time_series(self, alternative_time_series_data, quantile):
        temp_data = alternative_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').quantile(q=quantile)
        temp_data['time_step_id'] = temp_data.index

        return temp_data

    def __get_qt_agent_specific(self, agent_specific_data, quantile):
        temp_data = agent_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('agent_id').quantile(q=quantile)
        temp_data['agent_id'] = temp_data.index

        return temp_data

    def __get_qt_agent_time_series(self, agent_time_series_data, quantile):
        temp_data = agent_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').quantile(q=quantile)
        temp_data['time_step_id'] = temp_data.index

        return temp_data

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------- Methods to Extract SEM values for Data Series ----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def attach_sem_dataframes(self, alternative_specific_data, alternative_time_series_data,
                              agent_specific_data, agent_time_series_data,
                              target_alt_spec=None, target_alt_time=None,
                              target_agent_spec=None, target_agent_time=None):
        """attaches values for the standard error of the mean for four dataframes and types"""
        sem_alternative_specific = self.__attach_sem_alternative_specific(alternative_specific_data, target_alt_spec)
        sem_alternative_time = self.__attach_sem_alternative_time_series(alternative_time_series_data, target_alt_time)
        sem_agent_specific = self.__attach_sem_agent_specific(agent_specific_data, target_agent_spec)
        sem_agent_time = self.__attach_sem_agent_time_series(agent_time_series_data, target_agent_time)

        return sem_alternative_specific, sem_alternative_time, sem_agent_specific, sem_agent_time

    def __attach_sem_alternative_specific(self, alternative_specific_data, target_dataframe):
        temp_data = alternative_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('alternative_id').sem()
        temp_data['alternative_id'] = temp_data.index

        if isinstance(target_dataframe, pd.DataFrame):
            temp_data = target_dataframe.join(temp_data.drop('alternative_id', axis='columns').add_suffix('_sem'))

        return temp_data

    def __attach_sem_alternative_time_series(self, alternative_time_series_data, target_dataframe):
        temp_data = alternative_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').sem()
        temp_data['time_step_id'] = temp_data.index

        if isinstance(target_dataframe, pd.DataFrame):
            temp_data = target_dataframe.join(temp_data.drop('time_step_id', axis='columns').add_suffix('_sem'))

        return temp_data

    def __attach_sem_agent_specific(self, agent_specific_data, target_dataframe):
        temp_data = agent_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('agent_id').sem()
        temp_data['agent_id'] = temp_data.index

        if isinstance(target_dataframe, pd.DataFrame):
            temp_data = target_dataframe.join(temp_data.drop('agent_id', axis='columns').add_suffix('_sem'))

        return temp_data

    def __attach_sem_agent_time_series(self, agent_time_series_data, target_dataframe):
        temp_data = agent_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').sem()
        temp_data['time_step_id'] = temp_data.index

        if isinstance(target_dataframe, pd.DataFrame):
            temp_data = target_dataframe.join(temp_data.drop('time_step_id', axis='columns').add_suffix('_sem'))

        return temp_data

# ----------------------------------------------------------------------------------------------------------------------
# ------------------- Methods to Extract values for memory/heatmap related reporter variables---------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def get_single_simulation_memory_evolution(self, agent_set, duration):
        """extracts for the last simulation how the agents heatmaps fill up with data,
        this is merely Boolean information (0/1) and therefore only indicats if an agent has any knowledge on options,
        not the quality of these options"""
        temp_data = pd.DataFrame()                                                                                      # set up output data
        time_tracker = 0                                                                                                # set up time counter for loop functionality
        while time_tracker < duration:                                                                                  # loop over all time_steps
            time_data = {}

            for agent in agent_set.agents:
                time_data['time_step_id'] = str(time_tracker).zfill(len(str(duration)))
                time_data[agent] = len(agent_set.agents[agent].knowledge_evolution_tracker[time_data['time_step_id']])  # identify how many entries the heatmap has at a given time

            temp_data = temp_data.append(time_data, ignore_index=True)
            time_tracker += 1

        return temp_data

    def get_single_simulation_jaccard_matrices(self, agent_set, simulation_id=99):
        """constructs a dataframe with pairwise comparisons of amount of options that both agents gave knowledge on
        ,for all time steps in the model.
        With the similarity index being the Jaccard Index"""
        temp_data = pd.DataFrame()                                                                                      # prepare pandas dataframe for output
        input_data = agent_set.agents                                                                                   # define relevant data to extract from

        for time_id in list(agent_set.agents[next(iter(input_data))].knowledge_evolution_tracker.keys()):               # read from the first agent what time_steps it has logged in his tracker variable and loop over these time steps

            for agent_i in input_data:                                                                                  # loop for all pairwise comparisons involving agent i as compared to other agents
                temp_dict = defaultdict(str)                                                                            # prepare dictionary to load into pandas dataframe, if a key is accessed that is not present this key is made with a value of an empty list
                temp_dict['iteration_id'] = 'i_' + str(simulation_id)                                                   # attach iteration_id to row
                temp_dict['time_step_id'] = time_id                                                                     # attach time_id to row
                temp_dict['agent_i'] = agent_i                                                                          # attach agent_id of agent i to row
                heatmap_entries_i = set(list(input_data[agent_i].knowledge_evolution_tracker[time_id].keys()))          # define relevant data of agent i as the keys from the knowledge_evolution_tracker

                for agent_j in input_data:                                                                              # loop for all pairwise comparisons involving agent i as compared to another agent j
                    heatmap_entries_j = set(list(input_data[agent_j].knowledge_evolution_tracker[time_id].keys()))      # define relevant data of agent j as the keys from the knowledge_evolution_tracker

                    # calculate Jaccard index for similarity between two binary datasets
                    nb_shared_entries = len(heatmap_entries_i.intersection(heatmap_entries_j))                          # number of entries shared between agent i and j
                    nb_combined_entries = len(set.union(heatmap_entries_j, heatmap_entries_i))                          # number of entries that would be in the heatmap if agent i and j combined their heatmap
                    jaccard_i_j = nb_shared_entries/nb_combined_entries                                                 # Jaccard index as shared entries / combined entries
                    temp_dict[agent_j] = jaccard_i_j                                                                    # attach jaccard_i_j to temporary data

                temp_data = temp_data.append(temp_dict, ignore_index=True)                                              # load data from dictionary in pandas dataframe
        return temp_data                                                                                                # return pandas dataframe

    def get_average_competitor_data(self): #PLACEHOLDER
        pass
