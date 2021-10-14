from src.tools.model_tools.competition import CompetitionHandler
from src.tools.model_tools.agents import AgentSet, ForagerAgent
from src.tools.model_tools.choice_set import ChoiceSet, DiscreteAlternative
from src.config.init.init_objects import ObjectInitializer
from src.config.init.init_param import *

import numpy as np
import matplotlib.pyplot as plt

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
