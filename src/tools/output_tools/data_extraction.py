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
        aids runtime and readability"""

        self.functionality_extraction = self.__init_functionality_extraction()                                          # functionality to extract data as tracked by the model
        # TODO: Rename derived or deriving?
        self.functionality_derived_measures = self.__init_functionality_derived()                                       # functionality to calculate measures, indices etc. from data tracked by the model

    def __init_functionality_extraction(self):  # PLACE HOLDER FOR future reworking of the structure
        """intialises a dictionary containing all possible functionality
        for extracting and formatting directly tracked data in the model"""
        functionality = \
            {
                'generic_measures':
                    {
                        'iteration_tag': 'PLACEHOLDER'
                    },
                'alternative_spec':
                    {
                        'alternative_id': self.__extract_list_of_alternatives,
                        'alternative_cumulative_effort': self.__transform_alternative_effort_data,
                        'alternative_final_stock': self.__transform_final_stock_data
                        # INSERT FURTHER FUNCTIONALITY HERE
                    },
                'choice_set_time':
                    {
                        'time_series_id': self.__extract_list_of_time_steps
                        # INSERT FURTHER FUNCTIONALITY HERE
                    },
                'agent_spec':
                    {
                        'agent_id': self.__extract_list_of_agents,
                        'agent_cumulative_catch': self.__transform_agent_catch_data
                        # INSERT FURTHER FUNCTIONALITY HERE
                    },
                'agent_set_time':
                    {
                        'time_series_id': self.__extract_list_of_time_steps,
                        'yearly_catch': self.__transform_agent_set_total_catch_data
                        # INSERT FURTHER FUNCTIONALITY HERE
                    },
                'agent_spec_x_time_x_other':
                    {
                        'average_expected_competition': self.extract_average_expected_competition,
                        # INSERT FURTHER FUNCTIONALITY HERE
                    },
                'other_x_catch':
                    {
                        'catch': self.__extract_flat_agent_time_catch,
                        'competition': self.__extract_flat_agent_time_competition,
                        'knowledge_in_heatmap': self.__extract_flat_agent_time_knowledge,
                        'forage_option_visit': self.__extract_flat_agent_time_forage_option_visit,
                        'heatmap_expectation': self.__extract_flat_agent_time_heatmap_expectation,
                        'uncorrected_catch': self.__extract_flat_agent_time_uncorrected_catch,
                        'realised_competition': self.__extract_flat_agent_time_realised_competition
                        # INSERT FURTHER FUNCTIONALITY
                    }

                # INSERT POTENTIAL OTHER DATA TYPES HERE
            }
        return functionality

    def __init_functionality_derived(self):  # PLACEHOLDER for future reworking of the structure
        """intialises a dictionary containing all possible functionality
        for deriving measures (e.g. averages) from tracked data,
        often extracted in extraction functionality"""

        functionality = \
            {
                'average': self.get_average_dataframes,
                'standard deviation': self.get_sd_dataframes,
                'standard error of the mean': 'PLACEHOLDER',
                'median': 'PLACEHOLDER',
                'quantile': 'PLACEHOLDER',
                'min': 'PLACEHOLDER',
                'max': 'PLACEHOLDER'
            }
        return functionality
# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------- Main function to extract raw data series from model outputs -----------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def transform_output_data(self, choice_set, agent_set, duration, iteration_id=1):
        # TODO: agent_set = fleet(?) -- Ecodyn checken
        # TODO: choice_set = grid(?) -- Ecodyn checken
        """main functionality method, extracts data (currently hardcoded) from agents and choice options,
        producing pandas.Dataframe objects for a single iteration/simulation"""
        alternative_specific_data = self.__transform_alternative_data(choice_set, iteration_id)
        choice_set_time_series = self.__transform_alternative_time_series_data(choice_set, duration, iteration_id)
        agent_specific_data = self.__transform_agent_data(agent_set, iteration_id)
        agent_set_time_series = self.__transform_agent_time_series_data(agent_set, duration, iteration_id)

        return alternative_specific_data, choice_set_time_series, agent_specific_data, agent_set_time_series

# TODO KW: specific_data; what is specific data? you mean statistics over multpli iterations, such as averages etc? then that needs to be explained everywhere this is called
# TODO KW: time_series implies the value of a variable at a given time. if cumulative information is provided then 'cum' or such indication needs to be in the name.
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------- Subsections of the transform_output_data Method -------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __transform_alternative_data(self, choice_set, iteration_id=99):
        """ format choice_set data: effort and stock after fishing: aggregated over time step per grid cells"""
        temp_dictionary = dict()
        # create list with ID's of each alternative
        temp_dictionary['alternative_id'] = self.__extract_list_of_alternatives(choice_set)                             # attach choice option IDs as independent variables

        # currently implemented extractable data
        temp_dictionary['alternative_effort'] = self.__transform_alternative_effort_data(choice_set)                    # add response variable total effort exerted by agents over all time steps given to each specific choice option
        temp_dictionary['alternative_final_stock'] = self.__transform_final_stock_data(choice_set)                      # add data of final resource stock at the end of a simulation (as diagnostic data) for each choice option specific
        # add additional functionality HERE

        # change to DataFrame format
        alternative_data = pd.DataFrame(temp_dictionary)

        # add iteration_id to dataframe
        iteration_id = ['iteration_' + str(iteration_id)] * len(temp_dictionary['alternative_id'])                      # add a tag for the iteration an a data point originates from to each data point
        alternative_data.insert(0, 'iteration_id', iteration_id)                                                        # insert iteration ID as first column in the new data format

        return alternative_data

    def __transform_alternative_time_series_data(self, choice_set, duration, iteration_id=99):
        """ format choice_set data: Data aggregated over grid cells per time step"""
        # extract list of time_steps
        temp_dictionary = {}
        temp_dictionary['time_step_id'] = self.__extract_list_of_time_steps(duration)

        # currently implemented extractable data TODO: --FUNCTIONALITY-- implement examples for time_step alternative data
        # add additional functionality HERE

        # change to DataFrame format
        alternative_time_series_data = pd.DataFrame(temp_dictionary)

        # add iteration_id to dataframe
        iteration_id = ['iteration_' + str(iteration_id)] * len(temp_dictionary['time_step_id'])
        alternative_time_series_data.insert(0, 'iteration_id', iteration_id)

        return alternative_time_series_data

    def __transform_agent_data(self, agent_set, iteration_id=-99):
        """Format agent data : Data aggregated over time, per agent""" #TODO KW: per time step? then why the function below called time_series_data?
        # extract list of agent ID's
        temp_dictionary = dict()
        temp_dictionary['agent_id'] = self.__extract_list_of_agents(agent_set)

        # currently implemented extractable data
        #TODO KW: if this is total catch then use TotalCatch in the name of the function!
        #TODO KW: also specify if averaging over simulation occurred.
        temp_dictionary['agents_catch'] = self.__transform_agent_catch_data(agent_set)                                  # get agent specific total catch data (over all iteration time_steps) for each specific agent
        # add additional functionality HERE


        # change to DataFrame format
        alternative_time_series_data = pd.DataFrame(temp_dictionary)

        # add iteration_id to dataframe
        iteration_id = ['iteration_' + str(iteration_id)] * len(temp_dictionary['agent_id'])
        alternative_time_series_data.insert(0, 'iteration_id', iteration_id)

        return alternative_time_series_data

    def __transform_agent_time_series_data(self, agent_set, duration, iteration_id=99):
        """"function to retrieve data per time step for each agent and transform to usable format: catch data fleet"""
        # TODO: --STRUCTURAL-- near-duplicate of method transform_alternative_time_series_data, could be merged?
        # extract list of time_steps
        temp_dictionary = dict()
        temp_dictionary['time_step_id'] = self.__extract_list_of_time_steps(duration)

        # currently implemented extractable data
        temp_dictionary['total_catch'] = self.__transform_agent_set_total_catch_data(agent_set)
        # add additional functionality HERE

        # change to DataFrame format
        agent_time_series_data = pd.DataFrame(temp_dictionary)

        # add iteration_id to dataframe
        iteration_id = ['iteration_' + str(iteration_id)] * len(temp_dictionary['time_step_id'])
        agent_time_series_data.insert(0, 'iteration_id', iteration_id)

        return agent_time_series_data

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Internal Methods to Extract ID Data Series --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def __extract_list_of_time_steps(self, duration_model):
        """Obtain the time step ID"""
        time_steps = list()
        duration_counter = 0
        while duration_counter < duration_model:
            time_id = str(duration_counter).zfill(len(str(duration_model)))
            time_steps.append(time_id)
            duration_counter += 1

        return time_steps

    def __extract_list_of_alternatives(self, choice_set):
        """Obtain the list of alternative locations ID"""
        alternatives = list(choice_set.discrete_alternatives.keys())
        alternative_counter = 0
        while alternative_counter < len(alternatives):
            alternatives[alternative_counter] = alternatives[alternative_counter].split("_")[1]
            alternative_counter += 1

        return alternatives

    def __extract_list_of_agents(self, agent_set):
        """Obtain the agents ID's"""
        agents = list(agent_set.agents.keys())
        agent_counter = 0
        while agent_counter < len(agents):
            agents[agent_counter] = agents[agent_counter].split("_")[1]
            agent_counter += 1

        return agents
# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Internal Methods to Extract Actual Data Series -------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# TODO KW: actual data is extracted then call it extraction and not _transform_ happy to help fix this throughout the model, let me know!
    # TODO: Rename to extract
    def __transform_alternative_effort_data(self, choice_set):
        # Cumulative agents visits per grid cell
        effort_data = list(choice_set.effort_map.values())

        return effort_data

    def __transform_agent_catch_data(self, agent_set):
        """cumulative catch over time per agent"""
        catch_data = agent_set.agents

        # extract list of values for each agent
        catch = list()
        for agent in catch_data:
            catch.append(catch_data[agent].total_catch)

        return catch

    def __transform_agent_set_total_catch_data(self, agent_set):
        """catch of the fleet per time step"""
        # extract list of values for every time_step
        # TODO REPLACE TOTAL WITH FLEET
        time_step_catch = list(agent_set.total_time_step_catch_tracker.values())

        return time_step_catch

    def __transform_final_stock_data(self, choice_set):
        """Final stock in per grid cell"""
        final_stock_data = choice_set.discrete_alternatives

        final_stock = []
        for alternative in final_stock_data:
            final_stock.append(final_stock_data[alternative].resource_stock)

        return final_stock

    def __extract_time_step_catch_data(self, agent_set, time_step):
        """catch data per agent per time step"""
        catch_list = []
        data = agent_set.agents
        for agent in data:
            catch_list.append(data[agent].time_steps_catch[time_step])

        return catch_list

# TODO: quick and dirty fix for some basic measures, needs better flexibility through functionality dictionary
# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Methods to Create Average Data Series over Multiple Simulations---------------------
# ----------------------------------------------------------------------------------------------------------------------
    def get_average_dataframes(self, alternative_specific_data, alternative_time_series_data,
                               agent_specific_data, agent_time_series_data):
        """Create dataframes with averages"""
        avg_alternative_specific = self.__get_average_alternative_specific(alternative_specific_data)
        avg_alternative_time = self.__get_average_alternative_time_series(alternative_time_series_data)
        avg_agent_specific = self.__get_average_agent_specific(agent_specific_data)
        avg_agent_time = self.__get_average_agent_time_series(agent_time_series_data)

        return avg_alternative_specific, avg_alternative_time, avg_agent_specific, avg_agent_time

    def __get_average_alternative_specific(self, alternative_specific_data):
        """Average over iteration, for all trackers defined in class DiscreteAlternative,
        that have no temporal dimension"""
        temp_data = alternative_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('alternative_id').mean()
        temp_data['alternative_id'] = temp_data.index

        return temp_data

    def __get_average_alternative_time_series(self, alternative_time_series_data):
        """Average over iteration, for all trackers defined in class ChoiceSet,
        that have an explicit temporal dimension"""
        temp_data = alternative_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').mean()
        temp_data['time_step_id'] = temp_data.index

        return temp_data

    def __get_average_agent_specific(self, agent_specific_data):
        """Average over iteration, for all trackers defined in class ForagerAgent,
        that have no temporal dimension"""
        temp_data = agent_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('agent_id').mean()
        temp_data['agent_id'] = temp_data.index

        return temp_data

    def __get_average_agent_time_series(self, agent_time_series_data):
        """Average over iteration, for all trackers defined in class AgentSet,
        that have an explicit temporal dimension"""
        temp_data = agent_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').mean()
        temp_data['time_step_id'] = temp_data.index

        return temp_data

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------- Methods to Create standard deviation Data Series over Multiple Simulations ----------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def get_sd_dataframes(self, alternative_specific_data, alternative_time_series_data,
                               agent_specific_data, agent_time_series_data):
        """Create dataframes with standard deviation"""
        sd_alternative_specific = self.__get_sd_alternative_specific(alternative_specific_data)
        sd_alternative_time = self.__get_sd_alternative_time_series(alternative_time_series_data)
        sd_agent_specific = self.__get_sd_agent_specific(agent_specific_data)
        sd_agent_time = self.__get_sd_agent_time_series(agent_time_series_data)

        return sd_alternative_specific, sd_alternative_time, sd_agent_specific, sd_agent_time

    def __get_sd_alternative_specific(self, alternative_specific_data):
        """Standard deviation over iteration, for all trackers defined in class DiscreteAlternative,
        that have no temporal dimension"""
        temp_data = alternative_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('alternative_id').std()
        temp_data['alternative_id'] = temp_data.index

        return temp_data

    def __get_sd_alternative_time_series(self, alternative_time_series_data):
        """"Standard Deviation over iteration, for all trackers defined in class ChoiceSet,
        that have an explicit temporal dimension"""
        temp_data = alternative_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').std()
        temp_data['time_step_id'] = temp_data.index

        return temp_data

    def __get_sd_agent_specific(self, agent_specific_data):
        """Standard deviation over iteration, for all trackers defined in class ForagerAgent,
        that have no temporal dimension"""
        temp_data = agent_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('agent_id').std()
        temp_data['agent_id'] = temp_data.index

        return temp_data

    def __get_sd_agent_time_series(self, agent_time_series_data):
        """Standard deviation over iteration, for all trackers defined in class AgentSet,
        that have an explicit temporal dimension"""
        temp_data = agent_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').std()
        temp_data['time_step_id'] = temp_data.index

        return temp_data


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------- Methods to Extract Quantile values for Data Series -----------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def get_qt_dataframes(self, alternative_specific_data, alternative_time_series_data,
                          agent_specific_data, agent_time_series_data, quantile=0.95):
        #### TODO what happens here? ####
        qt_alternative_specific = self.__get_qt_alternative_specific(alternative_specific_data, quantile)
        qt_alternative_time = self.__get_qt_alternative_time_series(alternative_time_series_data, quantile)
        qt_agent_specific = self.__get_qt_agent_specific(agent_specific_data, quantile)
        qt_agent_time = self.__get_qt_agent_time_series(agent_time_series_data, quantile)

        return qt_alternative_specific, qt_alternative_time, qt_agent_specific, qt_agent_time

    def __get_qt_alternative_specific(self, alternative_specific_data, quantile):
        #### TODO what happens here? ####
        temp_data = alternative_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('alternative_id').quantile(q=quantile)
        temp_data['alternative_id'] = temp_data.index

        return temp_data

    def __get_qt_alternative_time_series(self, alternative_time_series_data, quantile):
        #### TODO what happens here? ####
        temp_data = alternative_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').quantile(q=quantile)
        temp_data['time_step_id'] = temp_data.index

        return temp_data

    def __get_qt_agent_specific(self, agent_specific_data, quantile):
        #### TODO what happens here? ####
        temp_data = agent_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('agent_id').quantile(q=quantile)
        temp_data['agent_id'] = temp_data.index

        return temp_data

    def __get_qt_agent_time_series(self, agent_time_series_data, quantile):
        #### TODO what happens here? ####
        temp_data = agent_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').quantile(q=quantile)
        temp_data['time_step_id'] = temp_data.index

        return temp_data

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------- Methods to Extract SEM values for Data Series TODO OVER SIMULATIONS, TIME STEPS, ETC?----------------------------------------------
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
        #### TODO what happens here? ####
        temp_data = alternative_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('alternative_id').sem()
        temp_data['alternative_id'] = temp_data.index

        if isinstance(target_dataframe, pd.DataFrame):
            temp_data = target_dataframe.join(temp_data.drop('alternative_id', axis='columns').add_suffix('_sem'))

        return temp_data

    def __attach_sem_alternative_time_series(self, alternative_time_series_data, target_dataframe):
        #### TODO what happens here? ####
        temp_data = alternative_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').sem()
        temp_data['time_step_id'] = temp_data.index

        if isinstance(target_dataframe, pd.DataFrame):
            temp_data = target_dataframe.join(temp_data.drop('time_step_id', axis='columns').add_suffix('_sem'))

        return temp_data

    def __attach_sem_agent_specific(self, agent_specific_data, target_dataframe):
        #### TODO what happens here? ####
        temp_data = agent_specific_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('agent_id').sem()
        temp_data['agent_id'] = temp_data.index

        if isinstance(target_dataframe, pd.DataFrame):
            temp_data = target_dataframe.join(temp_data.drop('agent_id', axis='columns').add_suffix('_sem'))

        return temp_data

    def __attach_sem_agent_time_series(self, agent_time_series_data, target_dataframe):
        #### TODO what happens here? ####
        temp_data = agent_time_series_data.drop('iteration_id', axis=1, inplace=False)
        temp_data = temp_data.groupby('time_step_id').sem()
        temp_data['time_step_id'] = temp_data.index

        if isinstance(target_dataframe, pd.DataFrame):
            temp_data = target_dataframe.join(temp_data.drop('time_step_id', axis='columns').add_suffix('_sem'))

        return temp_data

# ----------------------------------------------------------------------------------------------------------------------
# ------------------- Methods to Extract values for memory/heatmap related tracked variables ---------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def get_single_simulation_memory_evolution(self, agent_set, duration):
        """extracts for the last simulation how the agents\' heatmaps fill up with data,
        this only indicates if an agent has any knowledge on options,
        not the quality of these options"""
        temp_data = pd.DataFrame()                                                                                      # set up output data
        time_tracker = 0                                                                                                # set up time counter for loop functionality
        while time_tracker < duration:                                                                                  # loop over all time_steps
            time_data = {}

            # loop over agents to obtain the number of known alternatives for each time step.
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

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------ Extract Unaggregated Agent by Time data ---------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    # TODO: RENAME VARIABLES -- Catch irrelevant
    def get_other_x_catch(self, agent_set, iteration_id):      # NOT FINISHED
        """Extract unaggregated agent by time data for all implemented functionality"""
        data_output = pd.DataFrame()
        for data_series_extractor in self.functionality_extraction['other_x_catch']:                                    # loop over all data series, as potential explanatory variables to catch, we have functionality on in the functionality dictionary (quick and dirty fix, could be adapted to choose specific functionality)
            data_output = self.functionality_extraction['other_x_catch'][data_series_extractor](agent_set,
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

        return output_data

    def __extract_flat_agent_time_competition(self, agent_set, output_data=pd.DataFrame(), iteration_id=-99):
        """Extracts the average expected competition for every time step and agent"""
        # TODO: MERGE WITH Method above with duplicate functionality
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
# ---------------------- Methods to Extract Catch data for agent specific temporal patterns-----------------------------
# ----------------------------------------------------------------------------------------------------------------------
    # TODO: QUICK AND DIRTY WAY OF doing this DOUBLE CHECK DUPLICATE FUNCTIONALITY
    def extract_agent_time_catch(self, agent_set):
        #### TODO what happens here? is this catch or total catch?
        input_data = agent_set.agents
        output_data = {}

        time_data = []
        for time_id in tuple(input_data[next(iter(input_data))].time_step_catch.keys()):                                # loop over the items (time_steps) in an immutable list of time_steps as logged in the time_step_catch tracker of the first agent in the model
            time_data.append(time_id)
        output_data['time_id'] = time_data

        for agent in input_data:
            agent_catch_data = []
            for time_id in tuple(input_data[next(iter(input_data))].time_step_catch.keys()):                            # loop over the items (time_steps) in an immutable list of time_steps as logged in the time_step_catch tracker of the first agent in the model
                agent_catch_data.append(input_data[agent].time_step_catch[time_id])                                     # load time specific catch
            output_data[agent] = agent_catch_data

        output_data = pd.DataFrame(output_data)
        return output_data

# EOF