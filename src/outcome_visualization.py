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
        alternative_counter = 0
        while alternative_counter < len(alternatives):
            alternatives[alternative_counter] = alternatives[alternative_counter][-2:]
            alternative_counter += 1

        plt.bar(range(len(data)), values, tick_label=alternatives)
        plt.show()

    def make_agent_catch_graph(self, agent_set): # not Implemented yet
        pass
