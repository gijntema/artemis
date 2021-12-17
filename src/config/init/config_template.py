

template = {
    'model':
        {
            'duration': 50,
            'nb_iterations': 1,
            'reporting': False
        },
    'agents':
        {
            'nb_agents': 100,
            'catchability_coefficient': 0.2,
            'choice_method':
                {
                    'name': 'explore_weighted_heatmap',
                    'explore_attributes':
                        {
                            'explore_probability': 0.2,
                        },
                    'heatmap_attributes':
                        {
                            'init_nb_alternative_known': 4
                        }
                },
            'sharing':
                {
                    'sharing':
                        {
                            'name': 'random_sharing',
                            'no_sharing_attributes': 'DICTIONARY_PLACEHOLDER',
                            'random_sharing_attributes': 'DICTIONARY_PLACEHOLDER',
                            'nb_options_shared': 10
                        },
                    'receiver_choice':
                        {
                            'name': 'static_group_choice',
                            'group_attributes':
                                {
                                    'nb_groups': 1,
                                    'group_formation': "equal_mutually_exclusive_groups",
                                    'group_dynamics': False
                                },
                            'random_choice_attributes': 'DICTIONARY_PLACEHOLDER',
                            'nb_receivers': 10
                        },
                    'receiving':
                        {
                            'name': 'combine_receiver'
                        }
                },
        },
    'options':
        {
            'nb_options': 20,
            'growth':
                {
                    'growth_type': 'static',
                    'growth_attributes':
                        {
                            'growth_factor': 1
                        }

                },
            'stock_reset':
                {
                    'name': 'uniform_random_repeat',
                    'reset_probability': 0.1,
                    'uniform_attributes':
                        {
                            'min_stock': 0,
                            'max_stock': 200
                        },
                    'normal_attributes':
                        {
                            'init_stock': 100,
                            'sd_init_stock': 25
                        }
                }
        },
    'competition':
        {
            'name': 'interference-simple',
            'interference_attributes':
                {
                    'interference_factor': 0.8
                }
        }
}

#EOF