""""Basic tests to see if the modules are properly loaded; run with pytest."""

# import testing package and internal modules
from artemis.core.agents import ForagerAgent


def get_minimal_choice_set():
    class Alternative:
        resource_stock = 1

    class ChoiceSet:
        discrete_alternatives = {'alternative_0': Alternative()}
    
    return ChoiceSet()


def test_forageragent_initialization():
    """Test ForagerAgent initialization for minimal choice_set input."""
    agent = ForagerAgent(choice_set=get_minimal_choice_set(), choice_method='full_heatmap')
    assert type(agent.heatmap) is dict
    assert agent.heatmap['alternative_0'] == 0


def test_forageragent_update_trackers():
    """Test ForagerAgent.update_agent_trackers() for minimal choice_set input."""
    agent = ForagerAgent(choice_set=get_minimal_choice_set(), choice_method='full_heatmap')
    agent.time_step_catch[0] = 0
    assert agent.heatmap['alternative_0'] == 0
    assert agent.time_step_catch[0] == 0
    agent.update_agent_trackers('alternative_0', 1, 0)
    assert agent.heatmap['alternative_0'] == 1
    assert agent.time_step_catch[0] == 1


# If you want to run the test function directly.
if __name__ == "__main__":
    test_forageragent_initialization()
    test_forageragent_update_trackers()
