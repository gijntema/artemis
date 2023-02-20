from jsonschema import validate
import yaml
import os

# Locate schemas for config & agent.
SCHEMA_DIR = os.path.dirname(__file__)
CONFIG_SCHEMA_FILENAME = 'config_schema.yml'
AGENT_SCHEMA_FILENAME = 'agent_schema.yml'
CONFIG_SCHEMA_PATH = os.path.join(SCHEMA_DIR, CONFIG_SCHEMA_FILENAME)
AGENT_SCHEMA_PATH = os.path.join(SCHEMA_DIR, AGENT_SCHEMA_FILENAME)


def read_data_from_yml(filename):
    with open(filename) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


class Configuration:
    """Class to contain simulation configuration parameters."""

    _config_data: dict
    _agents: list

    def __init__(self, config_data):
        self._config_data = config_data
        config_schema = read_data_from_yml(CONFIG_SCHEMA_PATH)
        agent_schema = read_data_from_yml(AGENT_SCHEMA_PATH)
        validate(instance=self._config_data, schema=config_schema)
        self._agents = list(AgentConfiguration(agent, agent_schema) for agent in self._config_data['agents'])

    def to_yml(self, filename):
        """Save config data to yml file."""
        with open(filename, 'w') as file:
            yaml.dump(self._config_data, file, default_flow_style=False)

    @staticmethod
    def read_yml(filename):
        """Read config data from yml file."""
        config_data = read_data_from_yml(filename)
        return Configuration(config_data)

    @property
    def agents(self):
        return self._agents

    @property
    def name(self):
        return self._config_data['scenario_id']

    @property
    def duration(self):
        return self._config_data['model']['duration']

    @property
    def number_of_iterations(self):
        return self._config_data['model']['nb_iterations']

    @property
    def reporting(self):
        return self._config_data['model']['reporting']

    @property
    def choice_set_size(self):
        return self._config_data['options']['nb_options']

    @property
    def growth_type(self):
        return self._config_data['options']['growth']['growth_type']
        
    @property
    def growth_factor(self):
        return self._config_data['options']['growth']['growth_attributes']['growth_factor']

    @property
    def stock_reset_scenario(self):
        return self._config_data['options']['stock_reset']['name']

    @property
    def chance_reset_stock(self):
        return self._config_data['options']['stock_reset']['reset_probability']

    @property
    def min_stock(self):
        return self._config_data['options']['stock_reset']['uniform_attributes']['min_stock']

    @property
    def max_stock(self):
        return self._config_data['options']['stock_reset']['uniform_attributes']['max_stock']
        
    @property
    def init_stock(self):
        return self._config_data['options']['stock_reset']['normal_attributes']['init_stock']
        
    @property
    def sd_init_stock(self):
        return self._config_data['options']['stock_reset']['normal_attributes']['sd_init_stock']
        
    @property
    def competition_scenario(self):
        return self._config_data['competition']['name']
        
    @property
    def interference_factor(self):
        return self._config_data['competition']['interference_attributes']['interference_factor']

    @property
    def number_of_groups(self):
        return self._config_data['fleet']['receiver_choice']['group_attributes']['nb_groups']

    @property
    def division_style(self):
        return self._config_data['fleet']['receiver_choice']['group_attributes']['group_formation']

    @property
    def group_dynamics(self):
        return self._config_data['fleet']['receiver_choice']['group_attributes']['group_dynamics']

    @property
    def pick_receiver_strategy(self):
        return self._config_data['fleet']['receiver_choice']['name']


class AgentConfiguration:
    """Class to contain agent configuration parameters."""

    _agent_data: dict

    def __init__(self, agent_data, agent_schema):
        self._agent_data = agent_data
        validate(instance=self._agent_data, schema=agent_schema)

    @property
    def name(self):
        return self._agent_data['name']

    @property
    def number_of_agents(self):
        return self._agent_data['nb_agents']

    @property
    def catchability_coefficient(self):
        return self._agent_data['catchability_coefficient']

    @property
    def choice_method(self):
        return self._agent_data['choice_method']['name']

    @property
    def explore_probability(self):
        return self._agent_data['choice_method']['explore_attributes']['explore_probability']

    @property
    def init_number_of_alternatives_known(self):
        return self._agent_data['choice_method']['heatmap_attributes']['init_nb_alternative_known']

    @property
    def sharing_strategy(self):
        return self._agent_data['sharing']['sharing']['name']

    @property
    def shared_alternatives(self):
        return self._agent_data['sharing']['sharing']['nb_options_shared']

    @property
    def share_partners(self):
        return self._agent_data['sharing']['receiver_choice']['nb_receivers']

    @property
    def receiving_strategy(self):
        return self._agent_data['sharing']['receiving']['name']
