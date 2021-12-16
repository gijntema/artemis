from src.config.init.init_param import *

class ParamConverter:
    """Converts parameter names in the model to keys for use in the ConfigHandler object internal dictionaries
    and vice versa provides mapping to generate parameters from the ConfigHandler internal dictionaries object """

    def __init__(self):
        self.config_instructions = config_instructions = \
            [('model|duration', duration),
             ('model|nb_iterations', number_of_iterations),
             ('model|reporting', reporting),
             ('agents|nb_agents', number_of_agents),
             ('agents|catchability_coefficient', catchability_coefficient),
             ('agents|choice_method|name', choice_method),
             ('agents|choice_method|explore_attributes|explore_probability', explore_probability),
             ('agents|choice_method|heatmap_attributes|init_nb_alternative_known', init_number_of_alternatives_known),
             ('agents|sharing|sharing|name', sharing_strategy),
             ('agents|sharing|sharing|nb_options_shared', shared_alternatives),
             ('agents|sharing|sharing|no_sharing_attributes', 'DICTIONARY_PLACEHOLDER'),
             ('agents|sharing|sharing|random_sharing_attributes', 'DICTIONARY_PLACEHOLDER'),
             ('agents|sharing|receiver_choice|name', pick_receiver_strategy),
             ('agents|sharing|receiver_choice|group_attributes|nb_groups', number_of_groups),
             ('agents|sharing|receiver_choice|group_attributes|group_formation', division_style),
             ('agents|sharing|receiver_choice|group_attributes|group_dynamics', group_dynamics),
             ('agents|sharing|receiver_choice|random_choice_attributes', 'DICTIONARY_PLACEHOLDER'),
             ('agents|sharing|receiver_choice|nb_receivers', share_partners),
             ('agents|sharing|receiving|name', receiving_strategy),
             ('options|nb_options', choice_set_size),
             ('options|growth|growth_type', growth_type),
             ('options|growth|growth_attributes|growth_factor', growth_factor),
             ('options|stock_reset|name', stock_reset_scenario),
             ('options|stock_reset|reset_probability', chance_reset_stock),
             ('options|stock_reset|uniform_attributes|min_stock', min_stock),
             ('options|stock_reset|uniform_attributes|max_stock', max_stock),
             ('options|stock_reset|normal_attributes|init_stock', init_stock),
             ('options|stock_reset|normal_attributes|sd_init_stock', sd_init_stock),
             ('competition|name', competition_scenario),
             ('competition|interference_attributes|interference_factor', interference_factor)]

    def read_init_param_scenario(self):
        """reads the parameter values in init_param.py and converts them
        to parameter change instructions for the ConfigHandler object"""
        scenario_id = scenario_name
        return scenario_id, self.config_instructions

    def reverse_read_scenario(self, config_handler, scenario_id):  # UNIMPLEMENTED
        output_scenario_values = []
        for key, value in self.config_instructions:
            output_scenario_values.append(config_handler.get_config_value(config_key=key, scenario_id=scenario_id))

        return output_scenario_values
# EOF
