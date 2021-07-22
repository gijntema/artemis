import matplotlib.pyplot as plt


class GraphConstructor:

    def __init__(self):
        self.supported_graphs = []

    def make_graphs(self, agent_set, choice_set):

        effort_data_y, effort_data_x, effort_data_length, \
        agent_catch_y, agent_catch_x, agent_catch_data_length, \
        yearly_catch_y, yearly_catch_x, yearly_catch_data_length, \
        stock_y, stock_x, stock_data_length = \
            self.prepare_data(agent_set, choice_set)

        # insert four graphs for now
        # subplots stuff
        fig, axs = plt.subplots(2, 2)
        # Effort Graph
        axs[0, 0].bar(effort_data_x, effort_data_y)
        axs[0, 0].set_title('Effort per alternative')
        # agent catch graph
        axs[0, 1].bar(agent_catch_x, agent_catch_y)
        axs[0, 1].set_title('Catch per agent')
        # yearly catch graph
        axs[1, 0].plot(yearly_catch_x, yearly_catch_y)
        axs[1, 0].set_title('Catch per time step')
        # final resource stock graph
        axs[1, 1].bar(stock_x, stock_y)
        axs[1, 1].set_title('Final stock per alternative')


    def prepare_data(self, agent_set, choice_set):

        effort_data = choice_set.effort_map
        effort_data_length = len(effort_data)
        effort_data_y, effort_data_x = self.prepare_effort_data(effort_data)

        agent_catch_data = agent_set.agents
        agent_catch_data_length = len(agent_catch_data)
        agent_catch_y, agent_catch_x = self.prepare_agent_catch_data(agent_catch_data)

        yearly_catch_data = agent_set.total_yearly_catch_tracker
        yearly_catch_data_length = len(yearly_catch_data)
        yearly_catch_y, yearly_catch_x = self.prepare_total_catch_data(yearly_catch_data)

        stock_data = choice_set.discrete_alternatives
        stock_data_length = len(stock_data)
        stock_y, stock_x = self.prepare_stock_data(stock_data)

        return effort_data_y, effort_data_x, effort_data_length, \
               agent_catch_y, agent_catch_x, agent_catch_data_length, \
               yearly_catch_y, yearly_catch_x, yearly_catch_data_length, \
               stock_y, stock_x, stock_data_length

    def prepare_effort_data(self, effort_data):

        effort_x = list(effort_data.keys())
        effort_y = list(effort_data.values())
        # shorten the names of alternatives for clarity reason in the graph
        alternative_counter = 0
        while alternative_counter < len(effort_x):
            effort_x[alternative_counter] = effort_x[alternative_counter][-2:]
            alternative_counter += 1

        return effort_y, effort_x

    def prepare_agent_catch_data(self, agent_catch_data):
        agent_catch_x = list(agent_catch_data.keys())
        agent_catch_y = list()
        for agent in agent_catch_data:
            agent_catch_y.append(agent_catch_data[agent].total_catch)

        # shorten the names of agents for clarity reason in the graph
        agent_counter = 0
        while agent_counter < len(agent_catch_x):
            agent_catch_x[agent_counter] = agent_catch_x[agent_counter][-2:]
            agent_counter += 1

        return agent_catch_y, agent_catch_x

    def prepare_total_catch_data(self, yearly_catch_data):

        yearly_catch_x = list(yearly_catch_data.keys())
        yearly_catch_y = list(yearly_catch_data.values())
        time_step_counter = 0
        while time_step_counter < len(yearly_catch_x):
            yearly_catch_x[time_step_counter] = int(yearly_catch_x[time_step_counter])
            time_step_counter += 1

        return yearly_catch_y, yearly_catch_x

    def prepare_stock_data(self, stock_data):

        stock_x = list(stock_data.keys())
        stock_y = []
        for alternative in stock_data:
            stock_y.append(stock_data[alternative].resource_stock)

        alternative_counter = 0
        while alternative_counter < len(stock_x):
            stock_x[alternative_counter] = stock_x[alternative_counter][-2:]
            alternative_counter += 1

        return stock_y, stock_x

