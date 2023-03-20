"""
This Module is aimed at handling and executing how agents are ordered.
"""
import random

class AgentOrderer:

    def __init__(self, agent, strategy):

        self.agent_indices = agent.agent_index_list
        self.strategy = strategy
        self.functionality = self.__init_functionality()

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------- Define General Functionality --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def __init_functionality(self):
        functionality = \
            {
                "shuffle":
                    {
                        "execute": self.__order_shuffle
                    },
                "constant":
                    {
                        "execute": self.__order_none
                    }
            }
        return functionality

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------- Initialisation of Strategy Specific Ordering Functionality -------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def __order_none(self):
        return self.agent_indices

    def __order_shuffle(self):
        ordered_agent_indices = self.agent_indices.copy()
        random.shuffle(ordered_agent_indices)   
        return ordered_agent_indices

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------  Main Method to Order Agents -------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    def run_ordering(self):
        return self.functionality[self.strategy]["execute"]()
