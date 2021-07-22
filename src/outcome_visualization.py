import matplotlib.pyplot as plt


class GraphConstructor:

    def __init__(self):
        self.supported_graphs = []

    def make_graphs(self, agent_set, choice_set):
        self.make_choice_frequency_graph(choice_set)
        self.make_agent_catch_graph(agent_set)

    def make_choice_frequency_graph(self, choice_set):
        data = choice_set.effort_map
        alternatives = list(data.keys())
        values = list(data.values())
        # shorten the names of alternatives for clarity reason in the graph
        alternative_counter = 0
        while alternative_counter < len(alternatives):
            alternatives[alternative_counter] = alternatives[alternative_counter][-2:]
            alternative_counter += 1

        plt.bar(range(len(data)), values, tick_label=alternatives)
        plt.title('total effort exerted per Discrete alternative in the choice set')
        plt.show()

    def make_agent_catch_graph(self, agent_set):  # not Implemented yet
        data = agent_set.agents
        agents = list(data.keys())
        values = list()
        for agent in data:
            values.append(data[agent].total_catch)

        # shorten the names of agents for clarity reason in the graph
        agent_counter = 0
        while agent_counter < len(agents):
            agents[agent_counter] = agents[agent_counter][-2:]
            agent_counter += 1

        plt.bar(range(len(data)), values, tick_label=agents)
        plt.title('total catch per agent in the Agent Set')
        plt.show()

