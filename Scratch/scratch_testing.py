from src.tools.model_tools.competition import CompetitionHandler
from src.tools.model_tools.agents import AgentSet, ForagerAgent
from src.tools.model_tools.choice_set import ChoiceSet, DiscreteAlternative
from src.config.init.init_objects import ObjectInitializer
from src.config.init.init_param import *

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

competition_handler = CompetitionHandler('interference-simple')
# competition_handler = CompetitionHandler('absent')

object_initializer = ObjectInitializer()

number_of_agents = 10
sd_init_stock = 0.00000000000001
choice_set_size = 10
catchability_coefficient = 0.1

choice_set = object_initializer.initialize_choice_set(choice_set_size, init_stock, sd_init_stock, growth_factor)        # initialize the potential option in the model (e.g. the grid with cells to fish in)
agent_set = object_initializer.initialize_forager_agents(number_of_agents, choice_set,                                  # initialize the forager agents in the model (e.g. fishermen)
                                                         catchability_coefficient,
                                                         init_number_of_alternatives_known,
                                                         explore_probability, duration, choice_method)

for agent in agent_set.agents:
    alternative_index = agent_set.agents[agent].make_choice(choice_set)
    competition_handler.load_competition_data(alternative_index, agent)

for agent in agent_set.agents:
    competition_handler.competition_correction(choice_set, agent_set, agent, time_id=0)
    print(agent, ' catch:\t', agent_set.agents[agent].total_catch)
    print(agent, ' effort:\t', agent_set.agents[agent].forage_effort_tracker)

for choice_option in choice_set.effort_map:
    print(choice_option, ' :\t', choice_set.effort_map[choice_option])

print(competition_handler.relevant_data)
competition_handler.reset_relevant_data()
print(competition_handler.relevant_data)


# For furture reference to use a class type as key in dictionaries
from src.config.init.init_objects import ObjectInitializer
from collections import defaultdict

test_dictionary = defaultdict(int)
test_class = ObjectInitializer()
test_key = str(type(test_class)).split("'")[1].split(".")[-1]

print(test_key, " : ", test_dictionary[test_key])

# testing random normal random numbe rgenerator

mu, sigma = 100, 25
dataset = np.random.normal(loc=100, scale=25, size=100000)
count, bins, ignored = plt.hist(dataset, 30, density=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
         np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
         linewidth=2, color='r')
plt.show()


# ----------------------------------------------------------------------------------------------------------------------

def extract_time_x_group_catch(dataframe):
    data_dictionary = defaultdict(list)
    unique_values_time = dataframe['time_id'].unique()
    unique_values_group = dataframe['group_allegiance'].unique()
    for time_id in unique_values_time:
        time_temp_df = dataframe[dataframe.time_id == time_id]
        data_dictionary[time_id].append(time_id)
        for group in unique_values_group:
            temp_group_df = time_temp_df[dataframe.group_allegiance == group]
            data_dictionary[group].append(temp_group_df['catch'].sum())

    output_dataframe = pd.Dataframe(data_dictionary)
    return output_dataframe

# MAKE MAYTRIX PLOT FOR FORAGE VISITS PER ALTERNATIVE (Y) AND OVER TIME (X)
def extract__visualize_frequency_space_x_time_visits(dataframe):
    # Visualizing a heatmap plot for Space x Time forage visits
    df = dataframe  # Replace with other_x_catch_data when running after a ARTEMIS.py run
    output_df = pd.DataFrame()
    time_data_series = np.sort(df['time_id'].unique())
    output_df['time_id'] = time_data_series

    option_series = np.sort(df['forage_visit'].unique())
    for alternative in option_series:
        alternative_data_series = []
        for time in time_data_series:
            alternative_data_series.append(
                len(df.loc[(df['iteration_id'] == 0) & (df['time_id'] == time) & (df['forage_visit'] == alternative)]))
        output_df[alternative] = alternative_data_series

    df = output_df
    heatmap_data = []
    list_of_alternatives = list(df.columns)[1:]

    for column in list_of_alternatives:
        heatmap_data.append(df[column])

    fig = go.Figure(data=go.Heatmap(z=heatmap_data,
                                    y=list_of_alternatives,
                                    x=df['time_id']))
    #fig.update_layout(yaxis_title='forage_option',
    #                  x_axis_title='time')
    fig.show()
    fig.write_image("{}{}.png".format('forage_visit_matrix', '_test'))
