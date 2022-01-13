

template = {
                                                                                                                        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    'model':                                                                                                            # ------ General settings for the model --------
        {
            'duration': 50,                                                                                             # time a simulation runs for
            'nb_iterations': 1,                                                                                         # number fo iterations/simulation every scenario is tested for
            'reporting': False                                                                                          # indicates if a scenario run reports using all print statements in the script (False --> only report what scenario the model starts running and the total runtime)
        },                                                                                                              # ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    'agents':                                                                                                           # ------- Settings for the agents in the model -------
        {
            'nb_agents': 100,                                                                                           # the number of ForagerAgents that forage in the model
            'catchability_coefficient': 0.2,                                                                            # the fraction of the resource stock in a given choice option / DiscreteAlternative/ environment unit an agent receives if foraging there
            'choice_method':                                                                                            # settings for the way an agent chooses a choice option / DiscreteAlternative/ enviroment unit
                {
                    'name': 'explore_weighted_heatmap',                                                                 # name of the method an agent employs to choose a choice option / DiscreteAlternative/ enviromnent unit to forage in
                    'explore_attributes':                                                                               # settings if 'explore' is part of the method an agent employs to choose a choice option / DiscreteAlternative/ enviroment unit
                        {
                            'explore_probability': 0.2,                                                                 # the probability an agent uses picks a random choice option / DiscreteAlternative/ enviroment unit
                        },
                    'heatmap_attributes':                                                                               # settings if 'heatmap' is part of the method an agent employs to choose a choice option / DiscreteAlternative/ enviroment unit
                        {
                            'init_nb_alternative_known': 4                                                              # initial number of choice option / DiscreteAlternative/ enviroment unit an agent has information/memory an
                        }
                },
            'sharing':                                                                                                  # settings for the way an agent shares and receives information on choice option / DiscreteAlternative/ enviroment units with/from other agents
                {
                    'sharing':                                                                                          # settings for what information an agent shares with on choice option / DiscreteAlternative/ enviroment units
                        {
                            'name': 'random_sharing',                                                                   # name of the method an agent employs to determine what information on choice option / DiscreteAlternative/ enviroment unit to share with other agents
                            'no_sharing_attributes': 'DICTIONARY_PLACEHOLDER',                                          # placeholder for settings if 'no_sharing' is part of the method an agent employs to determine what information on choice option / DiscreteAlternative/ enviroment unit with other agents
                            'random_sharing_attributes': 'DICTIONARY_PLACEHOLDER',                                      # placeholder for settings if 'random_sharing' is part of the method an agent employs to determine what information on choice option / DiscreteAlternative/ enviroment unit with other agents
                            'nb_options_shared': 10                                                                     # number of choice option / DiscreteAlternative/ enviroment unit an agent shares information on with other agents every time unit
                        },
                    'receiver_choice':                                                                                  # settings for with whom an agent shares information on choice option / DiscreteAlternative/ enviroment units
                        {
                            'name': 'static_group_choice',                                                              # name of the method an agent employs to determine with whom to share information on choice option / DiscreteAlternative/ enviroment unit
                            'group_attributes':                                                                         # settings if 'group' is part of the method to determine with whom to share information on choice option / DiscreteAlternative/ enviroment units
                                {
                                    'nb_groups': 1,                                                                     # determine how many 'friend' groups of agents are in the model
                                    'group_formation': "equal_mutually_exclusive_groups",                               # determines the way 'friend' groups are formed at the start of a model run
                                    'group_dynamics': False                                                             # determines how 'friend' group might change over time (False is no change)
                                },
                            'random_choice_attributes': 'DICTIONARY_PLACEHOLDER',                                       # settings if 'random_choice' is part of the method to determine with whom to share information on choice option / DiscreteAlternative/ enviroment units
                            'nb_receivers': 10                                                                          # number of agents that an agent shares information with every unit of time
                        },
                    'receiving':                                                                                        # settings for how an agent receives/accepts information from other agents on choice option / DiscreteAlternative/ enviroment units
                        {
                            'name': 'combine_receiver'                                                                  # name of the method an agent employs to receive/accept information from other agents on choice option / DiscreteAlternative/ enviroment unit
                        }
                },
        },
                                                                                                                        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    'options':                                                                                                          # ------- Settings for the choice option / DiscreteAlternative/ enviroment units in the model -------
        {
            'nb_options': 20,                                                                                           # number of subdivisions of the environment (choice option / DiscreteAlternative/ enviroment units) (e.g. Grid cells) in the model and therefore the number of choices an agent has
            'growth':                                                                                                   # settings on the way stocks that can be foraged in different choice option / DiscreteAlternative/ enviroment units change over time
                {
                    'growth_type': 'static',                                                                            # the way stocks in choice option / DiscreteAlternative/ enviroment units change over time
                    'growth_attributes':                                                                                # additional settings on the way stocks in choice option / DiscreteAlternative/ enviroment units change over time
                        {
                            'growth_factor': 1                                                                          # speed of growth of stocks (per time unit) --> Stock(t+1) = Stock(t, growth_factor)
                        }
                },
            'stock_reset':                                                                                              # Settings for the way a stock in a choice option / DiscreteAlternative/ enviroment units resets (if it resets) at the end of a time unit t
                {
                    'name': 'uniform_random_repeat',                                                                    # the way a stock in a choice option / DiscreteAlternative/ enviroment units resets at the end of a time unit
                    'reset_probability': 0.1,                                                                           # the probability a stock in a choice option / DiscreteAlternative/ enviroment units resets at the end of a time unit
                    'uniform_attributes':                                                                               # settings if 'uniform' is in the way a stock in a choice option / DiscreteAlternative/ enviroment units is reset at the end of a time unit
                        {
                            'min_stock': 0,                                                                             # the minimum value a stock in a choice option / DiscreteAlternative/ enviroment units can get after a reset
                            'max_stock': 200                                                                            # the maximum value a stock in a choice option / DiscreteAlternative/ enviroment units can get after a reset
                        },
                    'normal_attributes':                                                                                # settings if 'normal' is in the way a stock in a choice option / DiscreteAlternative/ enviroment units is reset at the end of a time unit
                        {
                            'init_stock': 100,                                                                          # the mean value a stock in a stock in a choice option / DiscreteAlternative/ enviroment units can get after a reset
                            'sd_init_stock': 25                                                                         # the standard deviation of a value a stock in a choice option / DiscreteAlternative/ enviroment units can get after a reset
                        }
                }
        },
                                                                                                                        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    'competition':                                                                                                      # ------- settings for the way agents are hindered in foraging by other agents in the model -------
        {
            'name': 'interference-simple',                                                                              # the way agents are hindered in foraging by other agents in the model
            'interference_attributes':                                                                                  # settings if 'interference' is in the way agents are hindered in foraging by other agents in the model
                {
                    'interference_factor': 0.8                                                                          # the fraction foraging success is corrected for, for every other agent, if other agents choose the same choice option / DiscreteAlternative/ enviroment units to forage in in the same time unit
                }
        }
}                                                                                                                       # ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# EOF
