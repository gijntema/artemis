""""Basic tests to see if the modules are properly loaded; run with pytest."""

# import testing package and internal modules
from artemis.core.agents import ForagerAgent


def test_forageragent():
    """Test ForagerAgent initialization for minimal choice_set input."""
    class Alternative:
        resource_stock = 1

    class ChoiceSet:
        discrete_alternatives = {'alternative_0': Alternative()}

    agent = ForagerAgent(choice_set=ChoiceSet(), choice_method='full_heatmap')
    assert type(agent.heatmap) is dict
    assert agent.heatmap['alternative_0'] == 0
