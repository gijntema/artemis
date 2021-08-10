#
# This file is part of ARTEMIS (https://git.wur.nl/ecodyn/XXXX).
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

# TODO: Implement tests for all functionality of objects

# # import testing package and internal modules
import unittest
from src.agents import AgentSet, ForagerAgent, FishermanAgent, PredatorAgent
from src.choice_set import ChoiceSet, SpatialChoiceSet, DiscreteAlternative, SpatialGridCell
from src.config.init.init_objects import ObjectInitializer
from src.run_model import ModelRunner


class TestModelModules(unittest.TestCase):
    """class to test all functionality supported by the model"""

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Test AgentSet object functionality -------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

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

    def test_ForagerAgent_forage_maximalization(self):
        pass

    def test_ForagerAgent_forage_random(self):
        pass

    def test_ForagerAgent_basic_heatmap_optimalization(self):
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
        pass

    def test_PredatorAgent_inheritance(self):
        pass

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
# --------------------------------------------- Test ModelRunner Object functionality ------------------------------
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Run Tests --------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
