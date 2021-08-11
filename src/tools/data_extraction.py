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

# import external packages
import pandas as pd


# TODO: add desired functionality, only some examples of data are implemented for now:
# - Total Forage Effort per Alternative (check)
# - Final Resource Stock per Alternative
# - Total Catch per Agent
# - Yearly total industry/population catch

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------ Main Functionality Method ----------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class DataTransformer:
    """" Restructures the data outputs from the model to a usable data format (a pandas.Dataframe object)"""

    def transform_output_data(self, choice_set, agent_set, duration):
        alternative_specific_data = self.transform_alternative_data(choice_set)
        choice_set_time_series = self.transform_alternative_time_series_data(choice_set, duration)
        agent_specific_data = self.transform_agent_data(agent_set)
        agent_set_time_series = self.transform_agent_time_series_data(agent_set, duration)

        return alternative_specific_data, choice_set_time_series, agent_specific_data, agent_set_time_series
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------ Primary Subsections of the Main Functionality Method ----------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def transform_alternative_data(self, choice_set):
        # extract list of alternatives
        temp_dictionary = {}
        temp_dictionary['alternative_id'] = self.extract_list_of_alternatives(choice_set)

        # currently implemented extractable data
        temp_dictionary['alternative_effort'] = self.transform_alternative_effort_data(choice_set)
        temp_dictionary['alternative_final_stock'] = self.transform_final_stock_data(choice_set)
        # add additional functionality HERE

        # change to DataFrame format
        alternative_data = pd.DataFrame(temp_dictionary)
        return alternative_data

    def transform_alternative_time_series_data(self, choice_set, duration):
        # extract list of time_steps
        temp_dictionary = {}
        temp_dictionary['time_step_id'] = self.extract_list_of_time_steps(duration)

        # currently implemented extractable data - NONE so far # TODO: implement examples for yearly alternative data
        # add additional functionality HERE

        # change to DataFrame format
        alternative_time_series_data = pd.DataFrame(temp_dictionary)
        return alternative_time_series_data

    def transform_agent_data(self, agent_set):
        # extract list of time_steps
        temp_dictionary = {}
        temp_dictionary['agent_id'] = self.extract_list_of_agents(agent_set)

        # currently implemented extractable data
        temp_dictionary['agents_catch'] = self.transform_agent_catch_data(agent_set)
        # add additional functionality HERE

        # change to DataFrame format
        alternative_time_series_data = pd.DataFrame(temp_dictionary)
        return alternative_time_series_data

    def transform_agent_time_series_data(self, agent_set, duration):
        # TODO: method is is a near-duplicate of method transform_alternative_time_series_data, could be merged?
        # extract list of time_steps
        temp_dictionary = {}
        temp_dictionary['time_step_id'] = self.extract_list_of_time_steps(duration)

        # currently implemented extractable data - NONE so far # TODO: implement examples for yearly alternative data
        temp_dictionary['total_catch'] = self.transform_agent_set_total_catch_data(agent_set)
        # add additional functionality HERE

        # change to DataFrame format
        alternative_time_series_data = pd.DataFrame(temp_dictionary)
        return alternative_time_series_data

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Internal Methods to Extract Label Data Series --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def extract_list_of_time_steps(self, duration_model):
        years = list()
        duration_counter = 0
        while duration_counter < duration_model:
            years.append(str(duration_counter))
            duration_counter += 1

        return years

    def extract_list_of_alternatives(self, choice_set):
        alternatives = list(choice_set.discrete_alternatives.keys())
        alternative_counter = 0
        while alternative_counter < len(alternatives):
            alternatives[alternative_counter] = alternatives[alternative_counter].split("_")[1]
            alternative_counter += 1

        return alternatives

    def extract_list_of_agents(self, agent_set):
        agents = list(agent_set.agents.keys())
        agent_counter = 0
        while agent_counter < len(agents):
            agents[agent_counter] = agents[agent_counter].split("_")[1]
            agent_counter += 1

        return agents
# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------- Internal Methods to Extract Actual Data Series -------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def transform_alternative_effort_data(self, choice_set):

        effort_data = list(choice_set.effort_map.values())
        return effort_data

    def transform_agent_catch_data(self, agent_set):
        catch_data = agent_set.agents

        # extract list of values for each agent
        catch = list()
        for agent in catch_data:
            catch.append(catch_data[agent].total_catch)

        return catch

    def transform_agent_set_total_catch_data(self, agent_set):

        # extract list of values for every year
        yearly_catch = list(agent_set.total_yearly_catch_tracker.values())
        return yearly_catch

    def transform_final_stock_data(self, choice_set):
        final_stock_data = choice_set.discrete_alternatives

        final_stock = []
        for alternative in final_stock_data:
            final_stock.append(final_stock_data[alternative].resource_stock)

        return final_stock
