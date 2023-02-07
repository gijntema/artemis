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

# # import testing package and internal modules
import unittest
from artemis.core.agents import ForagerAgent, FishermanAgent, PredatorAgent


# TODO: rework module to pytest framework rather than unittest


class TestModelModules(unittest.TestCase):
    """class to test all functionality supported by the model"""

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- setup objects and parameters needed for testing ------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def setUp(self):
        pass

    def tearDown(self):
        pass

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Test AgentSet object functionality -------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def test_test(self):
        """" basic test to show how functionality of unittest is applied
        and to test if the modules are properly loaded"""

        agent = ForagerAgent()
        self.assertIsInstance(agent, ForagerAgent)

    def test_AgentSet_update_agent_trackers(self):
        pass

    def test_AgentSet_update_total_catch(self):
        pass

    def test_AgentSet_update_average_yearly_catch(self):
        pass

    def test_AgentSet_update_total_yearly_catch(self):
        pass
# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Test ForagerAgent object functionality ---------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def test_ForagerAgent_initialize_content(self):
        pass

    def test_ForagerAgent_initialize_choice_set_mirrors(self):
        pass

    def test_initialize_list_of_knowns(self):
        pass

    def test_ForagerAgent_initialize_fill_heatmap(self):
        pass

    def test_ForagerAgent_forage_maximalization(self):
        pass

    def test_ForagerAgent_forage_random(self):
        pass

    def test_ForagerAgent_forage_random_crowded(self):
        pass

    def test_ForagerAgent_basic_heatmap_optimalization(self):
        pass

    def test_ForagerAgent_crowded_heatmap_optimalization(self):
        pass

    def test_ForagerAgent_update_agent_trackers(self):
        pass

    def test_ForagerAgent_update_heatmap(self):
        pass

    def test_ForagerAgent_update_catch(self):
        pass

    def test_ForagerAgent_update_yearly_catch(self):
        pass

    def test_ForagerAgent_update_list_of_knowns(self):
        pass

    def test_ForagerAgent_share_heatmap_knowledge(self):
        pass

    def test_ForagerAgent_receive_heatmap_knowledge(self):
        pass
# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Test subclasses of ForagerAgent functionality --------------------------
# ----------------------------------------------------------------------------------------------------------------------

    def test_FishermenAgent_inheritance(self):
        fisher_agent = FishermanAgent()
        self.assertIsInstance(fisher_agent.heatmap, dict)

    def test_PredatorAgent_inheritance(self):
        predator_agent = PredatorAgent()
        self.assertIsInstance(predator_agent.heatmap, dict)

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Test ChoiceSet Object functionality ------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Test SpatialChoiceSet Object functionality -----------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Test DiscreteAlternative Object functionality --------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Test SpatialGridCell Object functionality ------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Test ObjectInitializer Object functionality ----------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Test ModelRunner Object functionality ----------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Run Tests --------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
